"""Tes endpoint /api/mahasiswa (status 200, 400, 404)."""
import pytest

URL = '/api/mahasiswa'
VALID = {
    'nim': '120140001',
    'nama': 'Ahmad Fauzi',
    'jurusan': 'Teknik Informatika',
    'tanggal_lahir': '2003-03-10',
    'alamat': 'Bandar Lampung',
}


def _tambah(testapp, **override):
    return testapp.post_json(URL, dict(VALID, **override)).json['data']


def test_list_kosong(testapp):
    assert testapp.get(URL, status=200).json == {'data': [], 'total': 0}


def test_list_berisi_data(testapp):
    _tambah(testapp)
    _tambah(testapp, nim='120140002', nama='Siti Aminah')
    res = testapp.get(URL, status=200)
    assert res.json['total'] == 2


def test_detail_ditemukan(testapp):
    baru = _tambah(testapp)
    res = testapp.get('%s/%d' % (URL, baru['id']), status=200)
    assert res.json['data']['nim'] == '120140001'
    assert res.json['data']['tanggal_lahir'] == '2003-03-10'


def test_detail_tidak_ditemukan_404(testapp):
    testapp.get(URL + '/9999', status=404)


def test_tambah_hanya_field_wajib(testapp):
    res = testapp.post_json(
        URL, {'nim': '1', 'nama': 'A', 'jurusan': 'B'}, status=200)
    assert res.json['data']['tanggal_lahir'] is None
    assert res.json['data']['alamat'] is None


@pytest.mark.parametrize('field', ['nim', 'nama', 'jurusan'])
def test_tambah_field_kurang_400(testapp, field):
    payload = {k: v for k, v in VALID.items() if k != field}
    testapp.post_json(URL, payload, status=400)


@pytest.mark.parametrize('tanggal', ['10-03-2003', 'kemarin', 20030310])
def test_tambah_tanggal_tidak_valid_400(testapp, tanggal):
    testapp.post_json(URL, dict(VALID, tanggal_lahir=tanggal), status=400)


def test_tambah_nim_duplikat_400(testapp):
    _tambah(testapp)
    testapp.post_json(URL, VALID, status=400)


def test_ubah_berhasil(testapp):
    baru = _tambah(testapp)
    res = testapp.put_json('%s/%d' % (URL, baru['id']),
                           {'jurusan': 'Sistem Informasi'}, status=200)
    assert res.json['data']['jurusan'] == 'Sistem Informasi'
    assert res.json['data']['nama'] == 'Ahmad Fauzi'


def test_ubah_tidak_ditemukan_404(testapp):
    testapp.put_json(URL + '/9999', {'nama': 'X'}, status=404)


def test_ubah_body_kosong_400(testapp):
    baru = _tambah(testapp)
    testapp.put_json('%s/%d' % (URL, baru['id']), {}, status=400)


def test_hapus_berhasil(testapp):
    baru = _tambah(testapp)
    testapp.delete('%s/%d' % (URL, baru['id']), status=200)
    testapp.get('%s/%d' % (URL, baru['id']), status=404)


def test_hapus_tidak_ditemukan_404(testapp):
    testapp.delete(URL + '/9999', status=404)


def test_halaman_home(testapp):
    res = testapp.get('/', status=200)
    assert '/api/matakuliah' in res.text
