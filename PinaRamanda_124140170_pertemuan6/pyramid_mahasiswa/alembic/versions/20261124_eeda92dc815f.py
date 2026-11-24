"""create matakuliah table

Revision ID: eeda92dc815f
Revises: 861355901cdf
Create Date: 2026-11-24 21:43:44.703363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeda92dc815f'
down_revision = '861355901cdf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'matakuliah',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kode_mk', sa.String(length=20), nullable=False),
        sa.Column('nama_mk', sa.String(length=100), nullable=False),
        sa.Column('sks', sa.Integer(), nullable=False),
        sa.Column('semester', sa.Integer(), nullable=False),
        sa.CheckConstraint(
            'semester > 0', name=op.f('ck_matakuliah_semester_positif')),
        sa.CheckConstraint(
            'sks > 0', name=op.f('ck_matakuliah_sks_positif')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_matakuliah')),
        sa.UniqueConstraint('kode_mk', name=op.f('uq_matakuliah_kode_mk')),
    )


def downgrade():
    op.drop_table('matakuliah')
