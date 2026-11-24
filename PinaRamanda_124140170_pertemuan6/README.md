# Praktikum Pemrograman Aplikasi Web - Pertemuan 6: Pyramid Framework

## Identitas Praktikan

| | |
|---|---|
| **Nama Lengkap** | Pina Ramanda |
| **NIM** | 124140170 |
| **Kelas** | RB |
| **Mata Kuliah** | Pemrograman Aplikasi Web (PAW) 2026/2027 T.A. Ganjil |
| **Program Studi** | Teknik Informatika, ITERA |

## Deskripsi Aplikasi

REST API sederhana yang dibangun dengan **Pyramid Framework**, **SQLAlchemy ORM**
dan **PostgreSQL**. Aplikasi menyediakan operasi CRUD (Create, Read, Update,
Delete) untuk dua resource:

1. **Mahasiswa** (`/api/mahasiswa`): materi praktikum.
2. **Matakuliah** (`/api/matakuliah`): **tugas pertemuan 6** (Manajemen Matakuliah).

Fitur utama:

- Migrasi skema database dengan **Alembic** (dua revisi: `create mahasiswa table`
  dan `create matakuliah table`).
- Seeding data awal (2 mahasiswa dan 4 matakuliah) lewat `initialize_db.py`.
- Validasi input dan status code yang tepat: `200` (sukses), `400` (input tidak
  valid/tidak lengkap) dan `404` (data tidak ditemukan).
- Transaksi otomatis dengan `pyramid_tm` + `zope.sqlalchemy`.
- Tes otomatis dengan `pytest` (71 tes) dan kode sesuai PEP 8 (`flake8` bersih).

## Teknologi

Python 3.10+ (diuji pada Python 3.13), Pyramid 2.x, SQLAlchemy 2.0, Alembic,
PostgreSQL, psycopg2, Waitress, Jinja2.

## Struktur Proyek

```text
Pina_Ramanda_124140170_pertemuan6/
├── development.ini
├── production.ini
├── pytest.ini
├── setup.py
├── MANIFEST.in
├── README.md
├── .gitignore
├── screenshots/                    # bukti pengujian untuk README
└── pyramid_mahasiswa/
    ├── __init__.py                 # factory aplikasi (main)
    ├── routes.py                   # definisi route + request_method
    ├── alembic/
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/               # revisi mahasiswa dan matakuliah
    ├── models/
    │   ├── __init__.py             # engine, session, registrasi model
    │   ├── meta.py                 # Base + naming convention
    │   ├── mahasiswa.py
    │   └── matakuliah.py
    ├── scripts/
    │   ├── __init__.py
    │   └── initialize_db.py        # seeding data awal
    ├── views/
    │   ├── __init__.py             # fungsi bantu validasi (bukan view)
    │   ├── default.py
    │   ├── mahasiswa.py
    │   └── matakuliah.py
    ├── templates/
    ├── static/
    └── tests/
```

## Langkah Instalasi

### 1. Prasyarat

- Python 3.10 atau lebih baru
- PostgreSQL (lokal, Docker, atau Postgres.app) dan client `psql`

### 2. Masuk ke folder dan buat virtual environment

```bash
cd Pina_Ramanda_124140170_pertemuan6
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\venv\Scripts\Activate.ps1
# Windows (CMD)
#   venv\Scripts\activate.bat
```

### 3. Pasang dependensi (mode editable)

```bash
pip install --upgrade pip
pip install -e ".[testing]"
```

### 4. Siapkan database PostgreSQL

Masuk ke `psql` sebagai superuser (mis. `sudo -u postgres psql`), lalu:

```sql
CREATE DATABASE pyramid_mahasiswa;
CREATE USER pyramid_user WITH PASSWORD 'pyramid_pass';
GRANT ALL PRIVILEGES ON DATABASE pyramid_mahasiswa TO pyramid_user;

-- Khusus PostgreSQL 15 ke atas:
\c pyramid_mahasiswa
GRANT ALL ON SCHEMA public TO pyramid_user;
ALTER DATABASE pyramid_mahasiswa OWNER TO pyramid_user;
```

URL koneksi ada di `development.ini`; ubah bila kredensial Anda berbeda:

```ini
sqlalchemy.url = postgresql://pyramid_user:pyramid_pass@localhost:5432/pyramid_mahasiswa
```

## Migrasi Database (Alembic)

```bash
# Menjalankan semua migrasi (membuat tabel mahasiswa dan matakuliah)
alembic -c development.ini upgrade head

# Melihat revisi aktif
alembic -c development.ini current
```

Revisi yang tersedia:

| Revisi | Pesan |
|---|---|
| `861355901cdf` | create mahasiswa table |
| `eeda92dc815f` | create matakuliah table |

Perintah lain yang berguna: `alembic -c development.ini downgrade -1`,
`upgrade +1`, dan `history`. Membuat revisi baru setelah mengubah model:

```bash
alembic -c development.ini revision --autogenerate -m "pesan revisi"
```

## Seeding Data Awal

```bash
initialize_pyramid_mahasiswa_db development.ini
```

Skrip ini aman dijalankan berulang kali (tidak menggandakan data). Hasilnya:
2 mahasiswa dan 4 matakuliah (`IF2101` sampai `IF2104`).

## Menjalankan Aplikasi

```bash
pserve development.ini --reload
```

Aplikasi berjalan di <http://localhost:6543>.

## Menjalankan Tes dan Cek PEP 8

```bash
pytest          # 71 tes; memakai SQLite in-memory, tidak perlu PostgreSQL
flake8 pyramid_mahasiswa setup.py   # pip install flake8 bila belum ada
```

## Dokumentasi Endpoint

### Mahasiswa

| Method | Endpoint | Fungsi | Status |
|---|---|---|---|
| GET | `/api/mahasiswa` | Daftar seluruh mahasiswa | 200 |
| GET | `/api/mahasiswa/{id}` | Detail mahasiswa | 200, 404 |
| POST | `/api/mahasiswa` | Tambah mahasiswa | 200, 400 |
| PUT | `/api/mahasiswa/{id}` | Ubah mahasiswa | 200, 400, 404 |
| DELETE | `/api/mahasiswa/{id}` | Hapus mahasiswa | 200, 404 |

Field: `nim` (unik, wajib), `nama` (wajib), `jurusan` (wajib),
`tanggal_lahir` (opsional, format `YYYY-MM-DD`), `alamat` (opsional).

### Matakuliah (tugas)

| Method | Endpoint | Fungsi | Status |
|---|---|---|---|
| GET | `/api/matakuliah` | Daftar seluruh matakuliah | 200 |
| GET | `/api/matakuliah/{id}` | Detail matakuliah | 200, 404 |
| POST | `/api/matakuliah` | Tambah matakuliah | 200, 400 |
| PUT | `/api/matakuliah/{id}` | Ubah matakuliah | 200, 400, 404 |
| DELETE | `/api/matakuliah/{id}` | Hapus matakuliah | 200, 404 |

Field: `kode_mk` (unik, wajib), `nama_mk` (wajib), `sks` (integer > 0, wajib),
`semester` (integer > 0, wajib).

Aturan validasi:

- `POST`: keempat field wajib ada; bila ada yang kurang, respons `400`.
- `sks` dan `semester` harus **integer positif**. Nilai `0`, negatif, desimal,
  string (`"3"`), dan boolean ditolak dengan `400`.
- `kode_mk` yang sudah dipakai ditolak dengan `400`.
- `PUT` hanya mengubah field yang dikirim (field lain tetap).
- `id` yang tidak ada atau tidak valid menghasilkan `404`.

Contoh respons sukses `POST /api/matakuliah`:

```json
{
  "message": "Matakuliah berhasil ditambahkan.",
  "data": {"id": 5, "kode_mk": "IF3101", "nama_mk": "Kecerdasan Buatan", "sks": 3, "semester": 6}
}
```

Contoh respons error: `{"error": "Field 'sks' harus lebih besar dari 0."}`

## Bukti Pengujian

Seluruh pengujian dijalankan dengan cURL terhadap server `pserve` yang
terhubung ke PostgreSQL.

### Migrasi, seeding, dan verifikasi `psql`

![Migrasi dan seeding](screenshots/00_migrasi_dan_seeding.png)

### Menjalankan server

![pserve](screenshots/01_pserve.png)

### Endpoint Mahasiswa

**GET daftar**

![GET list mahasiswa](screenshots/02_mahasiswa_get_list.png)

**GET detail (200 dan 404)**

![GET detail mahasiswa](screenshots/03_mahasiswa_get_detail.png)

**POST (200 dan 400)**

![POST mahasiswa](screenshots/04_mahasiswa_post.png)

**PUT (200 dan 404)**

![PUT mahasiswa](screenshots/05_mahasiswa_put.png)

**DELETE (200 dan 404)**

![DELETE mahasiswa](screenshots/06_mahasiswa_delete.png)

### Endpoint Matakuliah

**GET daftar**

![GET list matakuliah](screenshots/07_matakuliah_get_list.png)

**GET detail (200 dan 404)**

![GET detail matakuliah](screenshots/08_matakuliah_get_detail.png)

**POST (200 dan 400: sks nol, sks negatif, field kurang)**

![POST matakuliah](screenshots/09_matakuliah_post.png)

**PUT (200, 400, 404)**

![PUT matakuliah](screenshots/10_matakuliah_put.png)

**DELETE (200 dan 404)**

![DELETE matakuliah](screenshots/11_matakuliah_delete.png)

### Tes otomatis dan PEP 8

![pytest dan flake8](screenshots/12_pytest_dan_pep8.png)
