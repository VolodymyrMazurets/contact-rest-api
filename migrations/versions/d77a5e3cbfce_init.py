"""Init

Revision ID: d77a5e3cbfce
Revises: 4050886424ae
Create Date: 2024-03-06 10:36:04.957791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd77a5e3cbfce'
down_revision: Union[str, None] = '4050886424ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'additional_info',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'additional_info',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###
