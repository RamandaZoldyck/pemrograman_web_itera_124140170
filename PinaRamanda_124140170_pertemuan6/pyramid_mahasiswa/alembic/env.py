"""Konfigurasi lingkungan Alembic.

Dijalankan lewat: ``alembic -c development.ini <perintah>``.
URL database dibaca dari ``sqlalchemy.url`` pada bagian ``[app:main]``.
"""
from alembic import context
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config, pool

# Mengimpor paket models mendaftarkan semua model ke ``Base.metadata``
# sehingga ``--autogenerate`` dapat mendeteksi perubahan skema.
from pyramid_mahasiswa import models  # noqa: F401
from pyramid_mahasiswa.models.meta import Base

config = context.config

setup_logging(config.config_file_name)
settings = get_appsettings(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Menjalankan migrasi tanpa koneksi (menghasilkan SQL saja)."""
    context.configure(
        url=settings['sqlalchemy.url'],
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Menjalankan migrasi dengan koneksi database langsung."""
    engine = engine_from_config(
        settings, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
