"""
Modul member.py
Berisi class Member untuk merepresentasikan anggota perpustakaan.
Menerapkan konsep OOP (class dan encapsulation) untuk mengelola data anggota
serta daftar item yang dipinjam.
"""

from library_item import LibraryItem


class Member:
    """Merepresentasikan anggota perpustakaan yang dapat meminjam item."""

    def __init__(self, member_id: str, nama: str):
        """Menginisialisasi ID, nama anggota, dan daftar item pinjaman privat."""
        self._id = member_id
        self._nama = nama
        self.__daftar_pinjaman = []

    @property
    def id(self) -> str:
        """Mengembalikan ID anggota."""
        return self._id

    @property
    def nama(self) -> str:
        """Mengembalikan nama anggota."""
        return self._nama

    @property
    def daftar_pinjaman(self) -> list:
        """Mengembalikan daftar item yang sedang dipinjam (enkapsulasi salinan data)."""
        return list(self.__daftar_pinjaman)

    def pinjam_item(self, item: LibraryItem) -> bool:
        """Meminjam item dari perpustakaan dan mencatatnya ke daftar pinjaman anggota."""
        if not isinstance(item, LibraryItem):
            print("Gagal: Objek yang dipinjam harus turunan LibraryItem.")
            return False

        if item.is_dipinjam:
            print(f'Gagal: Item "{item.judul}" sedang dipinjam orang lain.')
            return False

        if item.pinjam():
            self.__daftar_pinjaman.append(item)
            print(f'Item "{item.judul}" berhasil ditambahkan ke daftar pinjaman {self.nama}.')
            return True
        return False

    def kembalikan_item(self, item: LibraryItem) -> bool:
        """Mengembalikan item dan menghapusnya dari daftar pinjaman anggota."""
        if item not in self.__daftar_pinjaman:
            print(f'Gagal: "{item.judul}" tidak ada dalam daftar pinjaman {self.nama}.')
            return False

        if item.kembalikan():
            self.__daftar_pinjaman.remove(item)
            print(f'Item "{item.judul}" berhasil dihapus dari daftar pinjaman {self.nama}.')
            return True
        return False

    def tampilkan_pinjaman(self) -> None:
        """Menampilkan seluruh item yang sedang dipinjam oleh anggota."""
        print(f"\n--- Pinjaman Aktif {self.nama} ({self.id}) ---")
        if not self.__daftar_pinjaman:
            print("Tidak ada item yang sedang dipinjam.")
            return

        for item in self.__daftar_pinjaman:
            print(f"- {item.get_detail()}")
