"""create mahasiswa table

Revision ID: 861355901cdf
Revises:
Create Date: 2026-11-24 21:43:43.193738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '861355901cdf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mahasiswa',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nim', sa.String(length=20), nullable=False),
        sa.Column('nama', sa.String(length=100), nullable=False),
        sa.Column('jurusan', sa.String(length=100), nullable=False),
        sa.Column('tanggal_lahir', sa.Date(), nullable=True),
        sa.Column('alamat', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_mahasiswa')),
        sa.UniqueConstraint('nim', name=op.f('uq_mahasiswa_nim')),
    )


def downgrade():
    op.drop_table('mahasiswa')
