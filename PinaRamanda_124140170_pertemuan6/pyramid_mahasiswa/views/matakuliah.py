"""View CRUD untuk resource Matakuliah (``/api/matakuliah``)."""
from pyramid.view import view_config

from ..models import Matakuliah
from . import (
    bad_request,
    clean_positive_int,
    clean_text,
    get_json_dict,
    not_found,
    parse_id,
)

REQUIRED_FIELDS = ('kode_mk', 'nama_mk', 'sks', 'semester')


def _get_or_404(request):
    mk_id = parse_id(request, 'Matakuliah')
    matakuliah = request.dbsession.get(Matakuliah, mk_id)
    if matakuliah is None:
        raise not_found('Matakuliah dengan id %d tidak ditemukan.' % mk_id)
    return matakuliah


def _validate(data, partial=False):
    """Memvalidasi body request dan mengembalikan dict nilai yang bersih.

    * POST (``partial=False``): ``kode_mk``, ``nama_mk``, ``sks`` dan
      ``semester`` wajib ada.
    * PUT (``partial=True``): hanya field yang dikirim yang divalidasi.
    * ``sks`` dan ``semester`` harus integer positif (> 0).
    """
    if not partial:
        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            raise bad_request(
                'Field wajib belum lengkap: %s.' % ', '.join(missing))
    elif not data:
        raise bad_request('Body request tidak boleh kosong.')

    cleaned = {}
    if 'kode_mk' in data:
        cleaned['kode_mk'] = clean_text(data, 'kode_mk', 20)
    if 'nama_mk' in data:
        cleaned['nama_mk'] = clean_text(data, 'nama_mk', 100)
    if 'sks' in data:
        cleaned['sks'] = clean_positive_int(data, 'sks')
    if 'semester' in data:
        cleaned['semester'] = clean_positive_int(data, 'semester')
    return cleaned


def _ensure_kode_unik(request, kode_mk, exclude_id=None):
    query = request.dbsession.query(Matakuliah).filter_by(kode_mk=kode_mk)
    if exclude_id is not None:
        query = query.filter(Matakuliah.id != exclude_id)
    if query.first() is not None:
        raise bad_request("Kode matakuliah '%s' sudah terdaftar." % kode_mk)


@view_config(route_name='matakuliah_list', renderer='json')
def matakuliah_list(request):
    """GET /api/matakuliah - daftar seluruh matakuliah."""
    rows = request.dbsession.query(Matakuliah).order_by(Matakuliah.id).all()
    return {'data': [row.to_dict() for row in rows], 'total': len(rows)}


@view_config(route_name='matakuliah_detail', renderer='json')
def matakuliah_detail(request):
    """GET /api/matakuliah/{id} - detail matakuliah (404 bila tidak ada)."""
    return {'data': _get_or_404(request).to_dict()}


@view_config(route_name='matakuliah_create', renderer='json')
def matakuliah_create(request):
    """POST /api/matakuliah - tambah matakuliah (400 bila tidak valid)."""
    cleaned = _validate(get_json_dict(request))
    _ensure_kode_unik(request, cleaned['kode_mk'])
    matakuliah = Matakuliah(**cleaned)
    request.dbsession.add(matakuliah)
    request.dbsession.flush()  # mengisi ``id`` sebelum respons dibuat
    return {'message': 'Matakuliah berhasil ditambahkan.',
            'data': matakuliah.to_dict()}


@view_config(route_name='matakuliah_update', renderer='json')
def matakuliah_update(request):
    """PUT /api/matakuliah/{id} - ubah data matakuliah."""
    matakuliah = _get_or_404(request)
    cleaned = _validate(get_json_dict(request), partial=True)
    if 'kode_mk' in cleaned:
        _ensure_kode_unik(
            request, cleaned['kode_mk'], exclude_id=matakuliah.id)
    for field, value in cleaned.items():
        setattr(matakuliah, field, value)
    request.dbsession.flush()
    return {'message': 'Matakuliah berhasil diubah.',
            'data': matakuliah.to_dict()}


@view_config(route_name='matakuliah_delete', renderer='json')
def matakuliah_delete(request):
    """DELETE /api/matakuliah/{id} - hapus matakuliah."""
    matakuliah = _get_or_404(request)
    request.dbsession.delete(matakuliah)
    return {'message': 'Matakuliah berhasil dihapus.'}
