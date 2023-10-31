"""initial

Revision ID: 34249f53b100
Revises: 
Create Date: 2023-10-31 07:56:55.483582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "34249f53b100"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("stock", sa.Integer, nullable=False),
        sa.Column("image", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("product")
