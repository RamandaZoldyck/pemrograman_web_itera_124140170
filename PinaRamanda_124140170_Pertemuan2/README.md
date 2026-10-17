1. Penjelasan Aplikasi

Bloomie adalah aplikasi dashboard mahasiswa yang digunakan untuk membantu mengelola tugas kuliah dan catatan dalam satu halaman.

Fitur-fitur yang tersedia pada aplikasi Bloomie:
- Menambahkan, mengedit, menghapus, dan menyelesaikan tugas.
- Memfilter tugas berdasarkan status.
- Menampilkan statistik tugas.
- Menambahkan dan menghapus catatan.
- Menyimpan data tugas dan catatan menggunakan Local Storage.
- Menampilkan informasi cuaca.
- Menampilkan kutipan motivasi.
- Mengambil data todo dari API.

2. Fitur ES6+ yang Digunakan

- Const dan Let: Digunakan untuk mendeklarasikan variabel. Contohnya const STORAGE_KEYS pada baris 1 dan const pada fungsi-fungsi lainnya.
- Class: Digunakan untuk membuat struktur objek aplikasi melalui class TaskItem pada baris 3 dan class DashboardApp pada baris 9.
- Constructor: Digunakan untuk menginisialisasi objek. Terdapat pada constructor() di baris 4 dan baris 10.
- Arrow Function: Digunakan untuk menulis fungsi dengan sintaks ringkas. Contohnya pada baris 21, task => new TaskItem(task), dan baris 42, event => { ... }.
- Template Literals: Digunakan untuk menggabungkan teks dengan variabel menggunakan tanda backtick (`). Contohnya pada baris 34, 37, dan 87.
- Default Parameters: Digunakan untuk memberikan nilai default pada parameter. Contohnya pada baris 4, seperti course = 'Umum', dueDate = '', dan completed = false.
- Destructuring: Digunakan untuk mengambil nilai dari objek atau array. Contohnya pada baris 15, const { ... } = e, serta baris 57, const { id } = event.target.dataset.
- Spread Operator: Digunakan untuk menyalin atau menggabungkan data array dan objek. Contohnya pada baris 48, [...this.tasks, new TaskItem(...)], dan pada baris 67, { ...task, completed: event.target.checked }.
- Object.assign(): Digunakan untuk menyalin properti objek ke objek lain. Contohnya pada baris 5, Object.assign(this, { ... }).
- Array Methods: Digunakan untuk mengolah data array. Contohnya:
- map() pada baris 21 untuk mengubah data tugas menjadi objek TaskItem.
- filter() pada baris 65 untuk menyaring tugas.
- find() pada baris 103 untuk mencari tugas berdasarkan ID.
- some() tidak digunakan dalam kode ini.
- Async/Await: Digunakan untuk menangani proses asynchronous saat mengambil data dari API. Contohnya pada baris 250, async loadExternalData(), dan baris 278, async loadWeather().
- Fetch API: Digunakan untuk mengambil data dari layanan eksternal. Contohnya pada baris 278 untuk cuaca Open-Meteo, baris 310 untuk kutipan DummyJSON, dan baris 325 untuk data todo JSONPlaceholder.
- Promise.allSettled(): Digunakan untuk menunggu seluruh proses pengambilan data API selesai, baik berhasil maupun gagal. Contohnya pada baris 256.
- Object.fromEntries(): Digunakan untuk mengubah array pasangan nilai menjadi objek. Contohnya pada baris 16 saat menghubungkan ID elemen HTML dengan elemen DOM.
- Nullish/Optional Chaining: Tidak ditemukan pada kode yang kamu kirim, sehingga tidak perlu dicantumkan.

3. Cara Menjalankan Aplikasi

- Buka folder proyek di Visual Studio Code.
- Jalankan file index.html menggunakan browser atau Live Server.
- Pastikan koneksi internet tersedia agar fitur API dapat digunakan.