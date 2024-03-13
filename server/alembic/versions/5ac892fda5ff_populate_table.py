"""populate table

Revision ID: 5ac892fda5ff
Revises: 542634da3739
Create Date: 2024-01-23 16:49:02.230475

"""
import csv
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert, delete
import csv
from app.models.model_stock import Stock

# revision identifiers, used by Alembic.
revision: str = '5ac892fda5ff'
down_revision: Union[str, None] = '542634da3739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open('app/db/current_day_close_prices.csv', 'r') as csv_file:
        conn = op.get_bind()
        csv_reader = csv.DictReader(csv_file)

        values_list = []
        for row in csv_reader:
            # Replace 'symbol_column' and 'price_column' with the actual column names in your CSV file
            stock_symbol = row['symbol']
            current_price = float(row['current_price']) if row['current_price'] not in ['N', ''] else None

            values_list.append({
                'symbol': stock_symbol,
                'current_price': current_price
            })

        if values_list:
            conn.execute(insert(Stock).values(values_list))



def downgrade() -> None:
    pass
