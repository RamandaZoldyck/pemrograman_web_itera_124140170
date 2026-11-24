"""Tes endpoint /api/matakuliah (status 200, 400, 404)."""
import pytest

URL = '/api/matakuliah'
VALID = {'kode_mk': 'IF1001', 'nama_mk': 'Algoritma', 'sks': 3, 'semester': 1}


def _tambah(testapp, **override):
    payload = dict(VALID, **override)
    return testapp.post_json(URL, payload).json['data']


def test_list_kosong(testapp):
    res = testapp.get(URL, status=200)
    assert res.json == {'data': [], 'total': 0}


def test_list_berisi_data(testapp):
    _tambah(testapp)
    _tambah(testapp, kode_mk='IF1002', nama_mk='Basis Data')
    res = testapp.get(URL, status=200)
    assert res.json['total'] == 2
    assert [m['kode_mk'] for m in res.json['data']] == ['IF1001', 'IF1002']


def test_detail_ditemukan(testapp):
    baru = _tambah(testapp)
    res = testapp.get('%s/%d' % (URL, baru['id']), status=200)
    assert res.json['data'] == baru


def test_detail_tidak_ditemukan_404(testapp):
    res = testapp.get(URL + '/9999', status=404)
    assert 'error' in res.json


@pytest.mark.parametrize('bad_id', ['abc', '0', '-1', '99999999999'])
def test_detail_id_tidak_valid_404(testapp, bad_id):
    testapp.get('%s/%s' % (URL, bad_id), status=404)


def test_tambah_berhasil_200(testapp):
    res = testapp.post_json(URL, VALID, status=200)
    data = res.json['data']
    assert data['id'] > 0
    assert data['kode_mk'] == 'IF1001'
    assert data['sks'] == 3


@pytest.mark.parametrize('field', ['kode_mk', 'nama_mk', 'sks', 'semester'])
def test_tambah_field_kurang_400(testapp, field):
    payload = {k: v for k, v in VALID.items() if k != field}
    res = testapp.post_json(URL, payload, status=400)
    assert field in res.json['error']


@pytest.mark.parametrize('field', ['sks', 'semester'])
@pytest.mark.parametrize('nilai', [0, -1, -10, 1.5, '3', None, True, []])
def test_tambah_integer_tidak_valid_400(testapp, field, nilai):
    testapp.post_json(URL, dict(VALID, **{field: nilai}), status=400)


@pytest.mark.parametrize('field', ['kode_mk', 'nama_mk'])
@pytest.mark.parametrize('nilai', ['', '   ', None, 123])
def test_tambah_teks_tidak_valid_400(testapp, field, nilai):
    testapp.post_json(URL, dict(VALID, **{field: nilai}), status=400)


def test_tambah_kode_duplikat_400(testapp):
    _tambah(testapp)
    res = testapp.post_json(URL, VALID, status=400)
    assert 'sudah terdaftar' in res.json['error']


def test_tambah_json_rusak_400(testapp):
    testapp.post(URL, 'bukan json', content_type='application/json',
                 status=400)


def test_tambah_body_bukan_object_400(testapp):
    testapp.post_json(URL, [1, 2, 3], status=400)


def test_ubah_berhasil(testapp):
    baru = _tambah(testapp)
    res = testapp.put_json(
        '%s/%d' % (URL, baru['id']),
        {'nama_mk': 'Algoritma Lanjut', 'sks': 4},
        status=200,
    )
    assert res.json['data']['nama_mk'] == 'Algoritma Lanjut'
    assert res.json['data']['sks'] == 4
    assert res.json['data']['kode_mk'] == 'IF1001'  # tidak berubah


def test_ubah_tidak_ditemukan_404(testapp):
    testapp.put_json(URL + '/9999', {'sks': 2}, status=404)


@pytest.mark.parametrize('payload', [
    {}, {'sks': 0}, {'sks': -2}, {'semester': 0}, {'semester': 'dua'},
    {'kode_mk': ''},
])
def test_ubah_tidak_valid_400(testapp, payload):
    baru = _tambah(testapp)
    testapp.put_json('%s/%d' % (URL, baru['id']), payload, status=400)


def test_ubah_kode_duplikat_400(testapp):
    _tambah(testapp)
    lain = _tambah(testapp, kode_mk='IF1002')
    testapp.put_json('%s/%d' % (URL, lain['id']),
                     {'kode_mk': 'IF1001'}, status=400)


def test_ubah_kode_sendiri_tidak_dianggap_duplikat(testapp):
    baru = _tambah(testapp)
    testapp.put_json('%s/%d' % (URL, baru['id']),
                     {'kode_mk': 'IF1001', 'sks': 2}, status=200)


def test_hapus_berhasil(testapp):
    baru = _tambah(testapp)
    testapp.delete('%s/%d' % (URL, baru['id']), status=200)
    testapp.get('%s/%d' % (URL, baru['id']), status=404)


def test_hapus_tidak_ditemukan_404(testapp):
    testapp.delete(URL + '/9999', status=404)


def test_method_tidak_didukung(testapp):
    # PATCH tidak punya route -> tidak boleh dipetakan ke view lain.
    testapp.patch_json(URL + '/1', {'sks': 2}, status=404)
