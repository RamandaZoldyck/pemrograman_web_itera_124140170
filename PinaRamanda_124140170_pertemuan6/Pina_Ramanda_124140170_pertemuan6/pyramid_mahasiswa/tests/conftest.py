"""Fixture pytest.

Tes memakai SQLite *in-memory* (tidak ada file ``.sqlite`` yang dibuat) agar
dapat dijalankan tanpa PostgreSQL.
"""
import pytest
import webtest
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from pyramid_mahasiswa import models
from pyramid_mahasiswa.models.meta import Base


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def bersihkan_tabel(engine):
    """Mengosongkan semua tabel sebelum setiap tes."""
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def testapp(engine):
    session_factory = models.get_session_factory(engine)

    with Configurator(settings={
        'tm.manager_hook': 'pyramid_tm.explicit_manager',
    }) as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')
        config.include('pyramid_mahasiswa.routes')
        config.add_request_method(
            lambda request: models.get_tm_session(
                session_factory, request.tm, request=request),
            'dbsession',
            reify=True,
        )
        config.scan('pyramid_mahasiswa.views')
        app = config.make_wsgi_app()

    return webtest.TestApp(app)
