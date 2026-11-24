from pyramid.view import view_config
from sqlalchemy.exc import SQLAlchemyError

ENDPOINTS = [
    ('GET', '/api/mahasiswa', 'Daftar seluruh mahasiswa'),
    ('GET', '/api/mahasiswa/{id}', 'Detail mahasiswa'),
    ('POST', '/api/mahasiswa', 'Tambah mahasiswa'),
    ('PUT', '/api/mahasiswa/{id}', 'Ubah mahasiswa'),
    ('DELETE', '/api/mahasiswa/{id}', 'Hapus mahasiswa'),
    ('GET', '/api/matakuliah', 'Daftar seluruh matakuliah'),
    ('GET', '/api/matakuliah/{id}', 'Detail matakuliah'),
    ('POST', '/api/matakuliah', 'Tambah matakuliah'),
    ('PUT', '/api/matakuliah/{id}', 'Ubah matakuliah'),
    ('DELETE', '/api/matakuliah/{id}', 'Hapus matakuliah'),
]


@view_config(route_name='home',
             renderer='pyramid_mahasiswa:templates/mytemplate.jinja2')
def home_view(request):
    return {'project': 'pyramid_mahasiswa', 'endpoints': ENDPOINTS}


@view_config(context=SQLAlchemyError, renderer='json')
def db_error_view(exc, request):
    """Kesalahan database yang tak terduga dikembalikan sebagai JSON 500."""
    request.response.status = 500
    return {'error': 'Terjadi kesalahan pada database.'}
