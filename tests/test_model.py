import unittest
import requests
import datetime
import logging
import json
logger = logging.getLogger()

cases = [
{
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
},
{
    "remote_ip": "89.70.56.64",
    "content": ["I am a bot!!!"],
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
},
{
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
    "social_media_user": {
        "verified": True,
        "geo_enabled": True,
        "protected": True,
        "pinned_tweet": True,
        "default_profile_image": True,
        "follower_count": 1000,
        "following_count": 50,
        "listed_count": 10,
        "tweet_count": 100,
        "created_at": str(datetime.datetime(2023, 12, 5, 14, 22, 20, 780245, tzinfo=datetime.timezone.utc))
    },
},
]

class BotDetectorClient:
    def __init__(self, base_url = "http://172.104.138.38:8000") -> None:
        self.base_url = base_url

    def get_threat(self, data):
        return requests.post(f"{self.base_url}/threat", data=json.dumps(data))


class TestThreatEndpoint:
    def __init__(self, test_cases: list[dict]) -> None:
        self.bot_detector = BotDetectorClient()
        self.test_cases = test_cases

    def run(self):
        self.test_empty_request()

    def test_empty_request(self):
        for case in self.test_cases:
            # bot_detected = case.pop("bot", None)
            response = self.bot_detector.get_threat(case)
            print(response.json())
            print()


if __name__ == "__main__":
    tests = TestThreatEndpoint(cases)
    tests.run()
