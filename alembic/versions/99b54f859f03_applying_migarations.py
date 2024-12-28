"""applying migarations

Revision ID: 99b54f859f03
Revises: a322d2bc26c6
Create Date: 2024-12-28 18:57:04.349257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '99b54f859f03'
down_revision: Union[str, None] = 'a322d2bc26c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('follow_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('follower_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('following_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['following_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('follow_id')
    )
    op.create_index(op.f('ix_follow_follower_id'), 'follow', ['follower_id'], unique=False)
    op.create_index(op.f('ix_follow_following_id'), 'follow', ['following_id'], unique=False)
    op.create_table('posts',
    sa.Column('post_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('caption', sa.String(length=255), nullable=False),
    sa.Column('post_media_url', sa.String(length=255), nullable=False),
    sa.Column('background_music_url', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('datetime_posted', sa.DateTime(), nullable=True),
    sa.Column('publisher_user_id', mysql.CHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['publisher_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('user_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('post_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_index(op.f('ix_comment_created_at'), 'comment', ['created_at'], unique=False)
    op.create_index(op.f('ix_comment_post_id'), 'comment', ['post_id'], unique=False)
    op.create_index(op.f('ix_comment_user_id'), 'comment', ['user_id'], unique=False)
    op.create_table('like',
    sa.Column('like_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('user_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('post_id', mysql.CHAR(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('like_id')
    )
    op.create_index(op.f('ix_like_post_id'), 'like', ['post_id'], unique=False)
    op.create_index(op.f('ix_like_user_id'), 'like', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_like_user_id'), table_name='like')
    op.drop_index(op.f('ix_like_post_id'), table_name='like')
    op.drop_table('like')
    op.drop_index(op.f('ix_comment_user_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_post_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_created_at'), table_name='comment')
    op.drop_table('comment')
    op.drop_table('posts')
    op.drop_index(op.f('ix_follow_following_id'), table_name='follow')
    op.drop_index(op.f('ix_follow_follower_id'), table_name='follow')
    op.drop_table('follow')
    # ### end Alembic commands ###