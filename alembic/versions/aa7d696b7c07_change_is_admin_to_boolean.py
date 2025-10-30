"""change is_admin to boolean

Revision ID: aa7d696b7c07
Revises: 7096d2dfff59
Create Date: 2025-10-28 12:19:44.274009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7d696b7c07'
down_revision: Union[str, Sequence[str], None] = '7096d2dfff59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
