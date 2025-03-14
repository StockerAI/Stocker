"""change columns types

Revision ID: 54d929ffb72e
Revises: 8a7b0d59b02b
Create Date: 2024-01-11 10:26:15.254074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54d929ffb72e'
down_revision: Union[str, None] = '8a7b0d59b02b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('CompanyDetails', 'targetHighPrice', existing_type=sa.Integer(), type_=sa.Float())
    op.alter_column('CompanyDetails', 'impliedSharesOutstanding', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade() -> None:
    pass
