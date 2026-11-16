"""
Modul library.py
Berisi class Library untuk mengelola koleksi item perpustakaan.
"""

from library_item import LibraryItem


class Library:
    """Mengelola penambahan, penampilan, dan pencarian item perpustakaan."""

    def __init__(self, nama: str):
        """Membuat perpustakaan dengan koleksi privat."""
        self.nama = nama
        self.__koleksi = []

    def tambah_item(self, item: LibraryItem) -> bool:
        """Menambahkan item baru dan mencegah ID yang sama."""
        if not isinstance(item, LibraryItem):
            print("Gagal: item harus merupakan turunan LibraryItem.")
            return False

        if any(data.id == item.id for data in self.__koleksi):
            print(f"Gagal: ID {item.id} sudah terdaftar.")
            return False

        self.__koleksi.append(item)
        print(f'Berhasil menambahkan "{item.judul}" ke perpustakaan.')
        return True

    def tampilkan_katalog(self, hanya_tersedia: bool = False) -> None:
        """Menampilkan seluruh koleksi atau hanya item yang tersedia."""
        judul_header = f"KATALOG ITEM TERSEDIA - {self.nama.upper()}" if hanya_tersedia else f"KATALOG {self.nama.upper()}"
        print(f"\n===== {judul_header} =====")
        daftar = [
            item for item in self.__koleksi
            if not hanya_tersedia or not item.is_dipinjam
        ]

        if not daftar:
            print("Tidak ada item yang dapat ditampilkan.")
            return

        # Polymorphism: setiap objek merespons get_detail() sesuai subclass-nya.
        for item in daftar:
            status = "Dipinjam" if item.is_dipinjam else "Tersedia"
            print(f"{item.get_detail()} | Status: {status}")

    def tampilkan_item_tersedia(self) -> None:
        """Menampilkan hanya item yang saat ini tersedia (tidak sedang dipinjam)."""
        self.tampilkan_katalog(hanya_tersedia=True)

    def cari_item(self, kata_kunci: str):
        """Mencari item berdasarkan ID atau judul (tidak membedakan kapital)."""
        kata_kunci = kata_kunci.strip().lower()
        hasil = [
            item for item in self.__koleksi
            if kata_kunci in item.id.lower()
            or kata_kunci in item.judul.lower()
        ]

        print(f'\nHasil pencarian "{kata_kunci}":')
        if not hasil:
            print("Item tidak ditemukan.")
            return []

        for item in hasil:
            status = "Dipinjam" if item.is_dipinjam else "Tersedia"
            print(f"{item.get_detail()} | Status: {status}")
        return hasil

    def get_item_by_id(self, item_id: str):
        """Mengambil objek item berdasarkan ID (tidak membedakan kapital)."""
        item_id = item_id.strip().lower()
        for item in self.__koleksi:
            if item.id.lower() == item_id:
                return item
        return None

    def pinjam_item(self, item_id: str) -> bool:
        """Memproses peminjaman item berdasarkan ID item."""
        item = self.get_item_by_id(item_id)
        if not item:
            print(f'Gagal: Item dengan ID "{item_id}" tidak ditemukan.')
            return False
        return item.pinjam()

    def kembalikan_item(self, item_id: str) -> bool:
        """Memproses pengembalian item berdasarkan ID item."""
        item = self.get_item_by_id(item_id)
        if not item:
            print(f'Gagal: Item dengan ID "{item_id}" tidak ditemukan.')
            return False
        return item.kembalikan()

    def get_jumlah_item(self) -> int:
        """Mengembalikan jumlah seluruh item yang tersimpan."""
        return len(self.__koleksi)
