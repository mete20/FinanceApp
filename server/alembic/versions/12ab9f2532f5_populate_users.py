"""populate users

Revision ID: 12ab9f2532f5
Revises: eea50379638c
Create Date: 2024-01-23 17:38:49.471539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert, delete
from faker import Faker
from app.models.model_user import User
from app.models.model_account import Account
from sqlalchemy.sql import select




# revision identifiers, used by Alembic.
revision: str = '12ab9f2532f5'
down_revision: Union[str, None] = 'eea50379638c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    fake = Faker()

    user_values_list = []
    for _ in range(100):  # Adjust the number of users you want to create
        user_values_list.append({
            'name': fake.user_name(),
            'mail': fake.email(),
            'password': fake.password()  # In a real application, ensure passwords are hashed
            # Add other fields as necessary
        })

    if user_values_list:
        conn.execute(insert(User).values(user_values_list))


def downgrade() -> None:
    pass
