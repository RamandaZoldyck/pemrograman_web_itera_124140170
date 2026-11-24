"""Definisi route aplikasi.

Setiap route memakai predikat ``request_method`` sehingga method HTTP yang
berbeda pada path yang sama dipetakan ke view yang tepat. Nama route di sini
harus sama persis dengan ``route_name`` pada ``@view_config``.
"""


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/', request_method='GET')

    # --- API Mahasiswa ---
    config.add_route(
        'mahasiswa_list', '/api/mahasiswa', request_method='GET')
    config.add_route(
        'mahasiswa_create', '/api/mahasiswa', request_method='POST')
    config.add_route(
        'mahasiswa_detail', '/api/mahasiswa/{id}', request_method='GET')
    config.add_route(
        'mahasiswa_update', '/api/mahasiswa/{id}', request_method='PUT')
    config.add_route(
        'mahasiswa_delete', '/api/mahasiswa/{id}', request_method='DELETE')

    # --- API Matakuliah ---
    config.add_route(
        'matakuliah_list', '/api/matakuliah', request_method='GET')
    config.add_route(
        'matakuliah_create', '/api/matakuliah', request_method='POST')
    config.add_route(
        'matakuliah_detail', '/api/matakuliah/{id}', request_method='GET')
    config.add_route(
        'matakuliah_update', '/api/matakuliah/{id}', request_method='PUT')
    config.add_route(
        'matakuliah_delete', '/api/matakuliah/{id}', request_method='DELETE')
