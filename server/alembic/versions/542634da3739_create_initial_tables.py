"""create initial tables

Revision ID: 542634da3739
Revises: bb19f3ddd6d4
Create Date: 2024-01-07 16:13:31.639402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '542634da3739'
down_revision: Union[str, None] = 'bb19f3ddd6d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('userID', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(length=255)),
        sa.Column('mail', sa.String(length=255)),
        sa.Column('password', sa.String(length=255)),
    )
    op.create_table('accounts',
        sa.Column('accountID', sa.Integer, primary_key=True, index=True),
        sa.Column('userID', sa.Integer, sa.ForeignKey('users.userID')),
        sa.Column('balance', sa.Float),
        sa.Column('balance_USD', sa.Float),
        sa.Column('current_stock_value', sa.Float)
    )
    op.create_table('watchlist',
        sa.Column('watchlistID', sa.Integer, primary_key=True, index=True),
        sa.Column('userID', sa.Integer, sa.ForeignKey('users.userID')),
        sa.Column('stockID', sa.Integer, sa.ForeignKey('stocks.id'))
    )
    op.create_table('portfolio',
        sa.Column('portfolioID', sa.Integer, primary_key=True, index=True),
        sa.Column('userID', sa.Integer, sa.ForeignKey('users.userID')),
        sa.Column('stockID', sa.Integer, sa.ForeignKey('stocks.id')),
        sa.Column('quantity', sa.Integer),
        sa.Column('averagePrice', sa.Float)
    )
    op.create_table('transactions',
        sa.Column('transactionID', sa.Integer, primary_key=True, index=True),
        sa.Column('userID', sa.Integer, sa.ForeignKey('users.userID')),
        sa.Column('stockID', sa.Integer, sa.ForeignKey('stocks.id')),
        sa.Column('quantity', sa.Integer),
        sa.Column('price', sa.Integer),
        sa.Column('timeStamp', sa.String(length=255)),
        sa.Column('type', sa.String(length=255))
    )
    op.create_table('news',
        sa.Column('newsID', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(length=255)),
        sa.Column('content', sa.String(length=255)),
        sa.Column('date', sa.String(length=255)),
        sa.Column('stockID', sa.Integer, sa.ForeignKey('stocks.id'))
    )
    
    pass


def downgrade() -> None:
    # downgrade the stock table to remove the name column
    pass
