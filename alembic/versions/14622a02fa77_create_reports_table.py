"""create reports table

Revision ID: 14622a02fa77
Revises: 1633fcd2790e
Create Date: 2024-04-22 11:07:27.115093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14622a02fa77'
down_revision: Union[str, None] = '1633fcd2790e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('reports',
                    sa.Column('id',sa.Integer(),nullable= False),
                    sa.Column('document_id',sa.Integer(),sa.ForeignKey('documents.id') ,nullable=False),
                    sa.Column('similarity_percentage', sa.VARCHAR, nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(), nullable= False)    
    )
    pass


def downgrade() -> None:
    pass
