"""Replace room size with description.

Revision ID: 7d2e4f5a6b7c
Revises: 93eb07a2a38f
Create Date: 2026-08-31
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7d2e4f5a6b7c"
down_revision = "93eb07a2a38f"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("chk_room_type_room_size_not_blank", "room_type", type_="check")
    op.alter_column(
        "room_type",
        "room_size",
        new_column_name="description",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "chk_room_type_description_not_blank",
        "room_type",
        "CHAR_LENGTH(TRIM(description)) > 0",
    )


def downgrade():
    op.drop_constraint("chk_room_type_description_not_blank", "room_type", type_="check")
    op.alter_column(
        "room_type",
        "description",
        new_column_name="room_size",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "chk_room_type_room_size_not_blank",
        "room_type",
        "CHAR_LENGTH(TRIM(room_size)) > 0",
    )
