"""Change totalAssets to bigint

Revision ID: 8a7b0d59b02b
Revises: 
Create Date: 2024-01-09 19:22:12.006969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a7b0d59b02b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('CompanyDetails', 'totalAssets', existing_type=sa.Integer(), type_=sa.BigInteger())


def downgrade() -> None:
    pass
