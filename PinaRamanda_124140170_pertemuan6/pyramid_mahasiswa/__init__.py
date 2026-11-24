"""Aplikasi CRUD Mahasiswa dan Matakuliah dengan Pyramid + PostgreSQL."""
from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    """Membuat dan mengembalikan aplikasi WSGI Pyramid."""
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        # Renderer JSON dengan indentasi agar mudah dibaca saat diuji.
        config.add_renderer('json', JSON(indent=2, ensure_ascii=False))
        config.include('.routes')
        config.include('.models')
        config.scan('.views')
    return config.make_wsgi_app()
