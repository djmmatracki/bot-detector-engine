from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(length=150), primary_key=True, index=True)
    username = Column(String(length=200), nullable=False)
    display_name = Column(String(length=200), nullable=True)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    verified = Column(Boolean, nullable=True)
    tweet_count = Column(Integer, default=0)
    listed_count = Column(Integer, default=0)
    default_profile_image = Column(Boolean, default=True)
    account_description = Column(String, nullable=True)
    geo_enabled = Column(Boolean, default=False)
    pinned_tweet = Column(Boolean, default=False)
    protected = Column(Boolean, default=False)
    description_urls_count = Column(Integer, default=0)
    description_mentions_count = Column(Integer, default=0)
    account_age_days = Column(Integer, default=0)
    average_tweets_per_day = Column(Integer, default=0)
    location = Column(String(length=250), nullable=True)
    bot = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship('Post', back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    lang = Column(String(length=10))
    like_count = Column(Integer)
    user_id = Column(String(length=150), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship('User', back_populates="posts")


class SessionRequest(Base):
    __tablename__ = "session_requests"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String(length=20))
    session_id = Column(UUID, nullable=False)
