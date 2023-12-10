import tensorflow as tf
import tensorflow_text as text
import numpy as np
from schemas import SocialMediaUser, RequestSample
from config import BROWSER_SIGNATURES, HTTP_COMMON_HEADERS
from datetime import datetime, timezone, timedelta
import pickle
import logging
logger = logging.getLogger()

class BotDetector:
    def __init__(self, text_model_path: str, user_model_path: str) -> None:
        self.text_model = tf.keras.models.load_model(text_model_path)
        with open(user_model_path, 'rb') as f:
            self.user_model = pickle.load(f)

    def verify_request(self, request: RequestSample) -> bool:
        data = {
            "remote_ip": "89.70.56.64",
            "content": [],
            "headers": {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,pl;q=0.7',
                'Access-Control-Request-Headers': 'authorization,content-type',
                'Access-Control-Request-Method': 'POST',
                'Connection': 'keep-alive',
                'Origin': 'https://social-media-app.onitsoft.com:8200',
                'Referer': 'https://social-media-app.onitsoft.com:8200/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
            },
            "connection_time": str(datetime.datetime(2023, 12, 5, 14, 22, 20, 780245, tzinfo=datetime.timezone.utc)),
            "connection_request_number": 1,
            "is_tls": True,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "tls_version": 772,
            "tls_handshake_complete": True,
            "tls_did_resume": True,
            "tls_cipher_suite": 4865,
            "tls_negotiated_protocol": "",
            "social_media_user": None,
        }
        # Check user agent
        if not any(browser in request.user_agent for browser in BROWSER_SIGNATURES):
            return True

        # Check if headers are unusual
        for key in request.headers.keys():
            if key not in HTTP_COMMON_HEADERS:
                return True

        # Check if connection time is malformed
        if (datetime.now(timezone.utc) - request.connection_time) > timedelta(minutes=10):
            return True

        # Check if connection_request_number is different than 1
        # if request.connection_request_number != 1:
        #     return True

        # Check if IP address is blacklisted
        return False

    async def verify_text(self, content: list[str]) -> float:
        threat = 0
        for text in content:
            if text == "":
                continue
            threat += float(tf.sigmoid(self.text_model(tf.constant([text])))[0][0])
        number_of_text = len(content) if len(content) != 0 else 1
        return threat / number_of_text

    async def verify_user(self, user: SocialMediaUser) -> float:
        account_age_days = (datetime.now(timezone.utc) - user.created_at).days + 1

        verified = int(user.verified)
        geo_enabled = int(user.geo_enabled)
        protected = int(user.protected)
        pinned_tweet = int(user.pinned_tweet)
        default_profile_image = int(user.default_profile_image)
        follower_count = user.follower_count
        following_count = user.following_count
        listed_count = user.listed_count
        average_tweets_per_day = np.round(user.tweet_count / account_age_days, 3)
        network = np.round(np.log(1 + average_tweets_per_day), 3)
        tweet_to_followers = np.round(np.log(1 + listed_count) * np.log(1 + follower_count), 3)
        hour_created = user.created_at.hour

        follower_acq_rate = np.round(
            np.log(1 + (follower_count / account_age_days)), 3)

        friends_acq_rate = np.round(
            np.log(1 + (following_count / account_age_days)), 3)
        
        favs_rate = np.round(np.log(1 + (following_count / account_age_days)), 3)

        user_features = [
            verified,
            geo_enabled,
            protected,
            pinned_tweet,
            default_profile_image, 
            follower_count, 
            following_count, 
            listed_count, 
            average_tweets_per_day,
            network, 
            tweet_to_followers, 
            follower_acq_rate, 
            friends_acq_rate,
            favs_rate,
            hour_created,
        ]
        result: np.int64 = self.user_model.predict([user_features])
        return int(result)
