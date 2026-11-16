"""
Modul main.py
Program utama sistem manajemen perpustakaan sederhana berbasis input pengguna:
- Menambahkan item ke perpustakaan (Buku dan Majalah)
- Menampilkan daftar item yang tersedia
- Mencari item berdasarkan judul atau ID
"""

import sys
import os

# Mencegah Python membuat folder __pycache__ secara otomatis saat program dijalankan
sys.dont_write_bytecode = True

# Memastikan modul lokal dapat diimpor dari direktori kerja mana pun
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from library_item import Book, Magazine
from library import Library


def main():
    """Menjalankan sistem manajemen perpustakaan berbasis input pengguna."""
    perpustakaan = Library("Perpustakaan ITERA")

    # Memasukkan data awal agar sistem langsung dapat diuji
    perpustakaan.tambah_item(Book("B001", "Laskar Pelangi", 2005, "Andrea Hirata", 529))
    perpustakaan.tambah_item(Book("B002", "Bumi Manusia", 1980, "Pramoedya Ananta Toer", 535))
    perpustakaan.tambah_item(Magazine("M001", "National Geographic", 2024, "Edisi Januari", "National Geographic"))

    while True:
        print("\n==========================================")
        print("   SISTEM MANAJEMEN PERPUSTAKAAN ITERA    ")
        print("==========================================")
        print("1. Menambahkan item ke perpustakaan")
        print("2. Menampilkan daftar item yang tersedia")
        print("3. Mencari item berdasarkan judul atau ID")
        print("0. Keluar")
        print("==========================================")

        try:
            pilihan = input("Pilih menu (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nProgram dihentikan.")
            break

        if pilihan == "1":
            print("\n--- Menambahkan Item ke Perpustakaan ---")
            print("Pilih jenis item:")
            print("1. Buku")
            print("2. Majalah")
            jenis = input("Pilihan (1/2): ").strip()

            if jenis == "1":
                try:
                    item_id = input("Masukkan ID Buku (misal B003): ").strip()
                    judul = input("Masukkan Judul Buku: ").strip()
                    tahun = int(input("Masukkan Tahun Terbit: "))
                    penulis = input("Masukkan Nama Penulis: ").strip()
                    halaman = int(input("Masukkan Jumlah Halaman: "))
                    buku = Book(item_id, judul, tahun, penulis, halaman)
                    perpustakaan.tambah_item(buku)
                except ValueError as e:
                    print(f"Gagal menambahkan buku: Input tidak valid ({e}).")

            elif jenis == "2":
                try:
                    item_id = input("Masukkan ID Majalah (misal M002): ").strip()
                    judul = input("Masukkan Judul Majalah: ").strip()
                    tahun = int(input("Masukkan Tahun Terbit: "))
                    edisi = input("Masukkan Edisi Majalah: ").strip()
                    penerbit = input("Masukkan Nama Penerbit: ").strip()
                    majalah = Magazine(item_id, judul, tahun, edisi, penerbit)
                    perpustakaan.tambah_item(majalah)
                except ValueError as e:
                    print(f"Gagal menambahkan majalah: Input tidak valid ({e}).")

            else:
                print("Pilihan jenis item tidak valid. Masukkan 1 untuk Buku atau 2 untuk Majalah.")

        elif pilihan == "2":
            perpustakaan.tampilkan_item_tersedia()

        elif pilihan == "3":
            kata_kunci = input("\nMasukkan kata kunci Judul atau ID: ").strip()
            if kata_kunci:
                perpustakaan.cari_item(kata_kunci)
            else:
                print("Kata kunci pencarian tidak boleh kosong.")

        elif pilihan == "0":
            print("\nProgram selesai. Terima kasih!")
            break

        else:
            print("\nPilihan tidak valid. Silakan pilih menu antara 0 sampai 3.")


if __name__ == "__main__":
    main()
