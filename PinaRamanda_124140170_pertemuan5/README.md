Nama Lengkap: Pina Ramanda
NIM: 124140170
Kelas Praktikum: RB

Deskripsi Program:
Program ini adalah sistem manajemen perpustakaan sederhana berbasis Python yang dirancang untuk mengelola koleksi buku dan majalah serta anggota perpustakaan. Alur program dimulai dari inisialisasi objek perpustakaan, penambahan item koleksi baru dengan validasi data dan pencegahan ID ganda, pendaftaran anggota, menampilkan daftar seluruh koleksi maupun item yang berstatus tersedia, melakukan transaksi peminjaman serta pengembalian item oleh anggota, dan mencari item berdasarkan judul maupun ID.

Penerapan 4 Pilar Object-Oriented Programming (OOP):
1. Class
Sistem mendefinisikan beberapa class yaitu LibraryItem sebagai class abstrak induk, Book dan Magazine sebagai class turunan yang merepresentasikan jenis item spesifik, Member untuk mengelola data anggota peminjam, serta Library sebagai class pengelola koleksi perpustakaan.

2. Inheritance
Class Book dan Magazine mewarisi seluruh sifat dari parent class LibraryItem. Kedua class anak memanfaatkan pemanggilan super().__init__() untuk menginisialisasi atribut dasar seperti id, judul, dan tahun terbit dari class induk, lalu menambahkan atribut spesifik seperti penulis dan jumlah halaman pada buku, serta edisi dan penerbit pada majalah.

3. Encapsulation
Perlindungan data diterapkan menggunakan access modifiers protected dan private. Atribut dasar menggunakan protected (_id, _judul, _tahun, _nama), sedangkan status peminjaman (__is_dipinjam) pada LibraryItem, koleksi item (__koleksi) pada Library, dan daftar pinjaman aktif (__daftar_pinjaman) pada Member menggunakan private. Akses pembacaan data penting disediakan melalui property decorator @property pada atribut id, judul, tahun, dan is_dipinjam. Perubahan nilai tahun terbit divalidasi melalui setter @tahun.setter, sementara status peminjaman hanya dapat diubah melalui method pinjam() dan kembalikan().

4. Polymorphism
Class induk LibraryItem menetapkan abstract method get_detail() yang wajib dioverride oleh setiap subclass. Class Book dan Magazine masing-masing mengimplementasikan get_detail() dengan format keluaran yang berbeda. Class Library dapat memanggil method get_detail() secara seragam pada seluruh item di dalam koleksi saat menampilkan katalog atau hasil pencarian tanpa perlu memeriksa tipe class objek secara manual.

Panduan Menjalankan Program:
1. Buka terminal pada folder tugas_perpustakaan, kemudian jalankan perintah berikut:
python main.py

2. Jika perintah python tidak dikenali pada perangkat Windows, gunakan perintah:
py main.py
