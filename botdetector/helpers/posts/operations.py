from helpers.posts.schemas import PostCreate
from db.models import Post


def create_post(db, post: PostCreate) -> Post:
    db_post = Post(
        text=post.text,
        user_id=post.user_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post():
    pass