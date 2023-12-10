from pydantic import BaseModel
import datetime

class TextSample(BaseModel):
    content: str

class SocialMediaUser(BaseModel):
    verified: bool
    geo_enabled: bool
    protected: bool
    pinned_tweet: bool
    default_profile_image: bool
    follower_count: int
    following_count: int
    listed_count: int
    tweet_count: int
    created_at: datetime.datetime

    # df['following_log'] = np.round(np.log(1 + df['following_count']), 3)
    # df['follower_log'] = np.round(np.log(1 + df['follower_count']), 3)
    # network = np.round(df['following_log'] * df['follower_log'], 3)

    # tweet_to_followers = np.round(np.log( 1+ df['listed_count']) * np.log(1+ df['follower_count']), 3)

    # account_age_days <- created_at
    # follower_acq_rate = np.round(np.log(1 + (df['follower_count'] / df['account_age_days'])), 3)

    # friends_acq_rate = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)
    # favs_rate = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)

class NetworkSample(BaseModel):
    pass

class RequestSample(BaseModel):
    remote_ip: str
    content: list[str]
    headers: dict[str, str]
    connection_time: datetime.datetime | str
    connection_request_number: int
    is_tls: bool
    user_agent: str
    tls_version: int
    tls_handshake_complete: bool
    tls_did_resume: bool
    tls_cipher_suite: int
    tls_negotiated_protocol: str
    social_media_user: SocialMediaUser | None
