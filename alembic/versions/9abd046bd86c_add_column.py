"""Add column

Revision ID: 9abd046bd86c
Revises: 54d929ffb72e
Create Date: 2024-01-12 15:15:34.524170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9abd046bd86c'
down_revision: Union[str, None] = '54d929ffb72e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('CompanyDetails', sa.Column('instrumentType', sa.String(), nullable=True))


def downgrade() -> None:
    pass
