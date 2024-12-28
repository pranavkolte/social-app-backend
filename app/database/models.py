import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    or_,
    ForeignKey, Text, Boolean,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from app.database import db


class Users(db.Base):
    __tablename__ = 'users'

    user_id = Column(
        CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    post_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "post_count": self.post_count,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "created_at": self.created_at
        }


    def save(self):
        with db.session() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except SQLAlchemyError as e:
                session.rollback()
                return None
            except Exception as e:
                session.rollback()
                return None

    @classmethod
    def get_user(cls, filter: dict, use_or: bool = False):
        with db.session() as session:
            try:
                if use_or:
                    filters = [
                        getattr(Users, key) == value
                        for key, value in filter.items()
                    ]
                    user = session.query(cls).filter(or_(*filters)).first()
                else:
                    user = session.query(cls).filter_by(**filter).first()
                return user
            except SQLAlchemyError as e:
                return None
            except Exception as e:
                return None


class Posts(db.Base):
    __tablename__ = 'posts'

    post_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    caption = Column(String(255), nullable=False)
    post_media_url = Column(String(255), nullable=False)
    background_music_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=False)
    datetime_posted = Column(DateTime, default=func.now())
    publisher_user_id = Column(CHAR(36), ForeignKey('users.user_id'), nullable=False)

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "caption": self.caption,
            "post_media_url": self.post_media_url,
            "background_music_url": self.background_music_url,
            "category": self.category,
            "datetime_posted": self.datetime_posted,
            "publisher_user_id": self.publisher_user_id
        }

    def save(self):
        with db.session() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except SQLAlchemyError as e:
                session.rollback()
                return None
            except Exception as e:
                session.rollback()
                return None

    @classmethod
    def get_posts_by_user(cls, user_id: str):
        with db.session() as session:
            try:
                posts = session.query(cls).filter_by(publisher_user_id=user_id).all()
                return posts
            except SQLAlchemyError:
                return None

    @classmethod
    def get_posts_by_user_list(cls, user_ids: list, limit: int = 10, offset: int = 0):
        with db.session() as session:
            try:
                posts = (
                    session.query(cls)
                    .filter(cls.publisher_user_id.in_(user_ids))
                    .order_by(cls.datetime_posted.desc())
                    .limit(limit)
                    .offset(offset)
                    .all()
                )
                return posts
            except SQLAlchemyError:
                return None

    @classmethod
    def get_post(cls, filter: dict, use_or: bool = False):
        with db.session() as session:
            try:
                if use_or:
                    filters = [
                        getattr(Posts, key) == value
                        for key, value in filter.items()
                    ]
                    post = session.query(cls).filter(or_(*filters)).first()
                else:
                    post = session.query(cls).filter_by(**filter).first()
                return post
            except SQLAlchemyError as e:
                return None
            except Exception as e:
                return None

    @classmethod
    def get_post_by_id(cls, post_id: str):
        with db.session() as session:
            try:
                post = session.query(cls).filter_by(post_id=post_id).first()
                return post
            except SQLAlchemyError:
                return None


class Like(db.Base):
    __tablename__ = "like"

    like_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    post_id = Column(
        CHAR(36),
        ForeignKey("posts.post_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=func.now())

    @classmethod
    def get_likes_for_post(cls, post_id: str, limit: int = 10, offset: int = 0):
        with db.session() as session:
            try:
                likes = (
                    session.query(cls)
                    .filter_by(post_id=post_id)
                    .order_by(cls.created_at.desc())
                    .limit(limit)
                    .offset(offset)
                    .all()
                )
                return likes
            except SQLAlchemyError:
                return []

    @classmethod
    def get_like_count(cls, post_id: str, user_id: str = None):
        with db.session() as session:
            try:
                count = session.query(cls).filter_by(post_id=post_id, user_id=user_id).count()
                return count
            except SQLAlchemyError:
                return 0

    def save(self):
        with db.session() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except SQLAlchemyError:
                session.rollback()
                return None

    @classmethod
    def delete(cls, post_id: str, user_id: str):
        with db.session() as session:
            try:
                like = session.query(cls).filter_by(post_id=post_id, user_id=user_id).first()
                if not like:
                    return False

                session.delete(like)
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False


class Follow(db.Base):
    __tablename__ = "follow"

    follow_id = Column(
        CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    follower_id = Column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    following_id = Column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "follow_id": self.follow_id,
            "follower_id": self.follower_id,
            "following_id": self.following_id,
            "created_at": self.created_at
        }

    def save(self):
        with db.session() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except SQLAlchemyError:
                session.rollback()
                return None

    @classmethod
    def get_follow(cls, filter: dict, use_or: bool = False):
        with db.session() as session:
            try:
                if use_or:
                    filters = [
                        getattr(Follow, key) == value
                        for key, value in filter.items()
                    ]
                    follow = session.query(cls).filter(or_(*filters)).first()
                else:
                    follow = session.query(cls).filter_by(**filter).first()
                return follow
            except SQLAlchemyError:
                return None

    @classmethod
    def get_following(cls, user_id: str):
        with db.session() as session:
            try:
                following = session.query(cls).filter_by(follower_id=user_id).all()
                return following
            except SQLAlchemyError:
                return None

    @classmethod
    def follow_user(cls, follower_id: str, following_id: str):
        existing_follow = cls.get_follow({
            "follower_id": follower_id,
            "following_id": following_id
        })
        if existing_follow:
            return cls.unfollow_user(existing_follow)
        else:
            return cls.create_follow(follower_id, following_id)

    @classmethod
    def create_follow(cls, follower_id: str, following_id: str):
        new_follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        ).save()
        return new_follow

    @classmethod
    def unfollow_user(cls, follow_instance):
        with db.session() as session:
            try:
                session.delete(follow_instance)
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False

class Comment(db.Base):
    __tablename__ = "comment"

    comment_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    post_id = Column(
        CHAR(36),
        ForeignKey("posts.post_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "like_count": self.like_count,
        }


    def save(self):
        with db.session() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except SQLAlchemyError:
                session.rollback()
                return None

    @classmethod
    def get_comments(cls, post_id: str, limit: int = 10, offset: int = 0):
        with db.session() as session:
            try:
                comments = (
                    session.query(cls)
                    .filter_by(post_id=post_id, is_active=True)
                    .order_by(cls.created_at.desc())
                    .limit(limit)
                    .offset(offset)
                    .all()
                )
                return comments
            except SQLAlchemyError:
                return []