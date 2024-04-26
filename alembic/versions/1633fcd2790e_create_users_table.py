"""create users table

Revision ID: 1633fcd2790e
Revises: 
Create Date: 2024-04-22 11:04:48.041592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1633fcd2790e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable= False),
                    sa.Column('username',sa.VARCHAR(),nullable=False),
                    sa.Column('email',sa.VARCHAR(), nullable= False),
                    sa.Column('phone_number',sa.VARCHAR(),nullable= False),
                    sa.Column('password',sa.VARCHAR(),nullable= False),
                    sa.Column('created_at',sa.TIMESTAMP(),nullable= False))
    pass


def downgrade() -> None:
    pass
