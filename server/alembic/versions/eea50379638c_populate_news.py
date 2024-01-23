"""populate news

Revision ID: eea50379638c
Revises: 5ac892fda5ff
Create Date: 2024-01-23 17:21:42.887071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert, delete
from faker import Faker
import random
from app.models.model_news import News



# revision identifiers, used by Alembic.
revision: str = 'eea50379638c'
down_revision: Union[str, None] = '5ac892fda5ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    fake = Faker()

    # Assuming you already have some stocks in your stocks table and their IDs are sequential starting from 1
    # Adjust the range as per your actual stock IDs
    stock_ids = range(1, 99)  # Example: 100 stocks

    news_values_list = []
    for _ in range(500):  # Example: Create 500 fake news entries
        news_values_list.append({
            'title': fake.sentence(nb_words=6),
            'content': fake.text(max_nb_chars=200),
            'date': fake.date(),
            'stockID': random.choice(stock_ids)
        })

    if news_values_list:
        conn.execute(insert(News).values(news_values_list))


def downgrade() -> None:
    pass
