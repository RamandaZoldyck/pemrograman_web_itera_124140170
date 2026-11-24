"""View CRUD untuk resource Mahasiswa (``/api/mahasiswa``)."""
from datetime import date

from pyramid.view import view_config

from ..models import Mahasiswa
from . import (
    bad_request,
    clean_text,
    get_json_dict,
    not_found,
    parse_id,
)

REQUIRED_FIELDS = ('nim', 'nama', 'jurusan')


def _get_or_404(request):
    mhs_id = parse_id(request, 'Mahasiswa')
    mahasiswa = request.dbsession.get(Mahasiswa, mhs_id)
    if mahasiswa is None:
        raise not_found('Mahasiswa dengan id %d tidak ditemukan.' % mhs_id)
    return mahasiswa


def _clean_tanggal(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise bad_request("Field 'tanggal_lahir' harus berformat YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise bad_request("Field 'tanggal_lahir' harus berformat YYYY-MM-DD.")


def _clean_alamat(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise bad_request("Field 'alamat' harus berupa teks.")
    return value.strip() or None


def _validate(data, partial=False):
    """Memvalidasi body request dan mengembalikan dict nilai yang bersih.

    Bila ``partial`` False (POST) semua field wajib harus ada. Bila True (PUT)
    hanya field yang dikirim yang divalidasi dan diubah.
    """
    if not partial:
        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            raise bad_request(
                'Field wajib belum lengkap: %s.' % ', '.join(missing))
    elif not data:
        raise bad_request('Body request tidak boleh kosong.')

    cleaned = {}
    if 'nim' in data:
        cleaned['nim'] = clean_text(data, 'nim', 20)
    if 'nama' in data:
        cleaned['nama'] = clean_text(data, 'nama', 100)
    if 'jurusan' in data:
        cleaned['jurusan'] = clean_text(data, 'jurusan', 100)
    if 'tanggal_lahir' in data:
        cleaned['tanggal_lahir'] = _clean_tanggal(data['tanggal_lahir'])
    if 'alamat' in data:
        cleaned['alamat'] = _clean_alamat(data['alamat'])
    return cleaned


def _ensure_nim_unik(request, nim, exclude_id=None):
    query = request.dbsession.query(Mahasiswa).filter_by(nim=nim)
    if exclude_id is not None:
        query = query.filter(Mahasiswa.id != exclude_id)
    if query.first() is not None:
        raise bad_request("NIM '%s' sudah terdaftar." % nim)


@view_config(route_name='mahasiswa_list', renderer='json')
def mahasiswa_list(request):
    """GET /api/mahasiswa - daftar seluruh mahasiswa."""
    rows = request.dbsession.query(Mahasiswa).order_by(Mahasiswa.id).all()
    return {'data': [row.to_dict() for row in rows], 'total': len(rows)}


@view_config(route_name='mahasiswa_detail', renderer='json')
def mahasiswa_detail(request):
    """GET /api/mahasiswa/{id} - detail satu mahasiswa."""
    return {'data': _get_or_404(request).to_dict()}


@view_config(route_name='mahasiswa_create', renderer='json')
def mahasiswa_create(request):
    """POST /api/mahasiswa - tambah mahasiswa baru."""
    cleaned = _validate(get_json_dict(request))
    _ensure_nim_unik(request, cleaned['nim'])
    mahasiswa = Mahasiswa(**cleaned)
    request.dbsession.add(mahasiswa)
    request.dbsession.flush()  # mengisi ``id`` sebelum respons dibuat
    return {'message': 'Mahasiswa berhasil ditambahkan.',
            'data': mahasiswa.to_dict()}


@view_config(route_name='mahasiswa_update', renderer='json')
def mahasiswa_update(request):
    """PUT /api/mahasiswa/{id} - ubah data mahasiswa."""
    mahasiswa = _get_or_404(request)
    cleaned = _validate(get_json_dict(request), partial=True)
    if 'nim' in cleaned:
        _ensure_nim_unik(request, cleaned['nim'], exclude_id=mahasiswa.id)
    for field, value in cleaned.items():
        setattr(mahasiswa, field, value)
    request.dbsession.flush()
    return {'message': 'Mahasiswa berhasil diubah.',
            'data': mahasiswa.to_dict()}


@view_config(route_name='mahasiswa_delete', renderer='json')
def mahasiswa_delete(request):
    """DELETE /api/mahasiswa/{id} - hapus mahasiswa."""
    mahasiswa = _get_or_404(request)
    request.dbsession.delete(mahasiswa)
    return {'message': 'Mahasiswa berhasil dihapus.'}
