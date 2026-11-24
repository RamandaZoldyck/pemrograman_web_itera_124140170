"""Mengisi data awal (seeding) ke database.

Pemakaian::

    initialize_pyramid_mahasiswa_db development.ini

Skrip ini idempotent: data yang sudah ada (berdasarkan ``nim`` / ``kode_mk``)
tidak akan ditambahkan dua kali.
"""
import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models import Mahasiswa, Matakuliah

DATA_MAHASISWA = [
    {
        'nim': '120140001',
        'nama': 'Ahmad Fauzi',
        'jurusan': 'Teknik Informatika',
        'tanggal_lahir': date(2003, 3, 10),
        'alamat': 'Jl. Contoh No. 1, Bandar Lampung',
    },
    {
        'nim': '120140002',
        'nama': 'Siti Aminah',
        'jurusan': 'Teknik Informatika',
        'tanggal_lahir': date(2003, 7, 21),
        'alamat': 'Jl. Contoh No. 2, Lampung Selatan',
    },
]

DATA_MATAKULIAH = [
    {'kode_mk': 'IF2101', 'nama_mk': 'Pemrograman Aplikasi Web',
     'sks': 3, 'semester': 5},
    {'kode_mk': 'IF2102', 'nama_mk': 'Basis Data',
     'sks': 3, 'semester': 3},
    {'kode_mk': 'IF2103', 'nama_mk': 'Struktur Data dan Algoritma',
     'sks': 4, 'semester': 3},
    {'kode_mk': 'IF2104', 'nama_mk': 'Pemrograman Berorientasi Objek',
     'sks': 3, 'semester': 2},
]


def _seed(dbsession, model, key, rows):
    """Tambahkan ``rows`` bila ``key`` belum ada di tabel."""
    for row in rows:
        exists = dbsession.query(model).filter_by(
            **{key: row[key]}).first()
        if exists is None:
            dbsession.add(model(**row))


def setup_models(dbsession):
    """Menambahkan data awal Mahasiswa dan Matakuliah."""
    _seed(dbsession, Mahasiswa, 'nim', DATA_MAHASISWA)
    _seed(dbsession, Matakuliah, 'kode_mk', DATA_MATAKULIAH)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='File konfigurasi, mis. development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Tidak dapat terhubung ke database. Periksa:

1. PostgreSQL sudah berjalan dan nilai ``sqlalchemy.url`` di file .ini benar.
2. Migrasi sudah dijalankan: alembic -c development.ini upgrade head
''')
        return 1
    print('Seeding selesai.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
