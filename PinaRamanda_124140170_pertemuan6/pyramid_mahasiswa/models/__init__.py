import zope.sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.orm import configure_mappers, sessionmaker

# Import semua model agar terdaftar pada ``Base.metadata`` (dipakai Alembic).
from .mahasiswa import Mahasiswa  # noqa: F401
from .matakuliah import Matakuliah  # noqa: F401
from .meta import Base  # noqa: F401

# Pastikan seluruh mapper sudah dikonfigurasi sebelum query pertama.
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager, request=None):
    """Membuat session yang terikat transaction manager.

    Session otomatis di-commit bila request sukses dan di-abort bila terjadi
    exception (dikelola ``pyramid_tm`` + ``zope.sqlalchemy``).
    """
    dbsession = session_factory(info={"request": request})
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """Dipanggil oleh ``config.include('.models')``."""
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    config.include('pyramid_tm')
    config.include('pyramid_retry')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # ``request.dbsession`` tersedia di setiap view.
    config.add_request_method(
        lambda request: get_tm_session(
            session_factory, request.tm, request=request),
        'dbsession',
        reify=True,
    )
