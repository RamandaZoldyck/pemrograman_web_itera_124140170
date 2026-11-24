"""Paket view dan fungsi bantu bersama untuk API JSON.

Fungsi di modul ini bukan view; hanya dipakai oleh ``views.mahasiswa`` dan
``views.matakuliah`` agar validasi dan format error konsisten.
"""
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

MAX_INT = 2147483647  # batas kolom INTEGER PostgreSQL


def bad_request(message):
    """Membuat respons 400 dengan body JSON ``{"error": ...}``."""
    return HTTPBadRequest(json_body={'error': message})


def not_found(message):
    """Membuat respons 404 dengan body JSON ``{"error": ...}``."""
    return HTTPNotFound(json_body={'error': message})


def get_json_dict(request):
    """Membaca body JSON; harus berupa object (dict), selain itu 400."""
    try:
        data = request.json_body
    except ValueError:
        raise bad_request('Body request harus berupa JSON yang valid.')
    if not isinstance(data, dict):
        raise bad_request('Body request harus berupa JSON object.')
    return data


def parse_id(request, label):
    """Mengambil ``{id}`` dari URL sebagai int; 404 bila tidak valid."""
    raw = request.matchdict['id']
    try:
        value = int(raw)
    except ValueError:
        raise not_found('%s dengan id %r tidak ditemukan.' % (label, raw))
    if not 0 < value <= MAX_INT:
        raise not_found('%s dengan id %r tidak ditemukan.' % (label, raw))
    return value


def clean_text(data, field, max_length):
    """Validasi string wajib: tidak kosong dan tidak melebihi panjang kolom."""
    value = data[field]
    if not isinstance(value, str) or not value.strip():
        raise bad_request("Field '%s' harus berupa teks yang tidak kosong."
                          % field)
    value = value.strip()
    if len(value) > max_length:
        raise bad_request("Field '%s' maksimal %d karakter."
                          % (field, max_length))
    return value


def clean_positive_int(data, field):
    """Validasi integer positif (> 0). ``bool`` dan string ditolak."""
    value = data[field]
    if isinstance(value, bool) or not isinstance(value, int):
        raise bad_request("Field '%s' harus berupa bilangan bulat." % field)
    if value <= 0:
        raise bad_request("Field '%s' harus lebih besar dari 0." % field)
    if value > MAX_INT:
        raise bad_request("Field '%s' terlalu besar." % field)
    return value
