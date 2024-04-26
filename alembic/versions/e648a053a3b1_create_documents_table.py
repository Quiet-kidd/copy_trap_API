"""create documents table

Revision ID: e648a053a3b1
Revises: 14622a02fa77
Create Date: 2024-04-22 11:10:05.482967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e648a053a3b1'
down_revision: Union[str, None] = '14622a02fa77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('documents',
                    sa.Column('id',sa.Integer(),nullable= False),
                    sa.Column('user_id',sa.Integer(), sa.ForeignKey('users.id'), nullable= False),
                    sa.Column('title', sa.VARCHAR, nullable=False),
                    sa.Column('content', sa.VARCHAR, nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(), nullable= False)
    )
    pass


def downgrade() -> None:
    pass
