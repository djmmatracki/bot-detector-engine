from sqlalchemy.orm import Session
from typing import List
from db.models import User
from helpers.users.schemas import UserCreate


def create_user(db, user: UserCreate) -> User:
    db_user = User(
        id=user.id,
        username=user.username,
        follower_count=user.follower_count,
        location=user.location,
        verified=user.verified,
        bot=user.bot,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, bot: bool | None = None) -> List[User]:
    if bot is not None:
        return db.query(User).filter(User.bot == bot).all()
    return db.query(User).all()
