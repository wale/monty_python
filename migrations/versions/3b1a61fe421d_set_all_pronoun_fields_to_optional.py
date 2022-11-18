"""set all pronoun fields to optional

Revision ID: 3b1a61fe421d
Revises: 15ac40aa23f5
Create Date: 2022-11-18 17:07:23.559699

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "3b1a61fe421d"
down_revision = "15ac40aa23f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("pronoun", "subj", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("pronoun", "obj", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("pronoun", "posDet", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("pronoun", "posPro", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("pronoun", "refl", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("pronoun", "refl", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("pronoun", "posPro", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("pronoun", "posDet", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("pronoun", "obj", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("pronoun", "subj", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###