"""Create users table

Revision ID: 6fe5285a1c28
Revises: 
Create Date: 2022-06-19 15:58:54.971593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from auth.hash import Hash

# revision identifiers, used by Alembic.
revision = '6fe5285a1c28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = op.create_table('users',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )

    op.bulk_insert(
        users_table,
        [
            {
                "user_id": uuid.UUID("00000000-0000-4000-a000-000000000000"),
                "username": "admin",
                "password": Hash.get_password_hash("admin"),
                "is_active": True,
                "is_admin": True
            }
        ]
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
