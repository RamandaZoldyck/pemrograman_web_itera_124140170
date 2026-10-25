# Shelf — Aplikasi Manajemen Buku Pribadi

Shelf adalah aplikasi React untuk mencatat buku yang sudah dimiliki, sedang dibaca, atau ingin dibeli. Antarmuka menggunakan warna  lembut, kartu buku, ringkasan koleksi, dan halaman statistik.

## Fitur
- Tambah buku dengan judul, penulis, dan status.
- Edit dan hapus buku (penghapusan meminta konfirmasi).
- Filter berdasarkan status dan cari berdasarkan judul atau penulis.
- Data disimpan di `localStorage` sehingga tetap tersedia setelah halaman dimuat ulang.
- Halaman Perpustakaan dan Statistik menggunakan React Router.
- Validasi input wajib isi dengan pesan error dan penanda visual.
- Tampilan responsif untuk desktop dan ponsel.

## Instalasi dan menjalankan
Pastikan Node.js sudah terpasang. Buka terminal VS Code di folder project, lalu jalankan:

```bash
npm install
npm run dev
```

Buka URL lokal yang ditampilkan Vite (biasanya `http://localhost:5173`).

Jika PowerShell memblokir `npm.ps1`, gunakan perintah Windows berikut:

```powershell
npm.cmd install
npm.cmd run dev
```

## Menjalankan unit test
Jalankan seluruh test satu kali:

```bash
npm.cmd run test:run
```

Atau mode watch:

```bash
npm.cmd test
```

Test mencakup tampilan input form, validasi kolom kosong, submit data valid, tampilan data buku, aksi edit, dan empty state. Setelah menjalankan test, ambil screenshot terminal sebagai bukti laporan testing dan lampirkan di laporan pengumpulan.

## Teknologi React yang digunakan
- **Functional components dan Hooks:** `useState` mengelola form, filter, pencarian, dan mode edit. `useEffect` menyinkronkan form saat mode edit berubah dan menyimpan data melalui custom hook.
- **Context API:** `BookContext` membagikan koleksi dan fungsi tambah/edit/hapus ke komponen yang membutuhkan.
- **React Router:** navigasi halaman Perpustakaan (`/`) dan Statistik (`/stats`).
- **Custom hooks:** `useLocalStorage` untuk persistensi dan `useBookStats` untuk menghitung ringkasan.
- **Reusable components:** `BookForm`, `BookList`, dan `BookFilter` dipakai untuk memisahkan fungsi UI.
- **PropTypes:** pemeriksaan tipe props diterapkan pada seluruh komponen UI dan provider.
- **Unit testing:** Vitest, React Testing Library, dan jest-dom untuk pengujian perilaku komponen.

## Struktur folder
```text
src/
├── components/
│   ├── BookForm/BookForm.jsx
│   ├── BookList/BookList.jsx
│   └── BookFilter/BookFilter.jsx
├── context/BookContext.jsx
├── hooks/
│   ├── useLocalStorage.js
│   └── useBookStats.js
├── pages/
│   ├── Home/Home.jsx
│   └── Stats/Stats.jsx
├── test/
│   ├── BookForm.test.jsx
│   ├── BookList.test.jsx
│   └── setup.js
├── App.jsx
├── main.jsx
└── styles.css
```

## Screenshot antarmuka
Jalankan aplikasi dengan `npm run dev`, lalu ambil screenshot halaman Perpustakaan dan Statistik di browser. Simpan screenshot tersebut pada dokumen/laporan pengumpulan. Screenshot aktual tidak disertakan otomatis karena harus diambil dari aplikasi yang sudah dijalankan di perangkat.
