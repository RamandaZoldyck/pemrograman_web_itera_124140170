"""
Modul library_item.py
Berisi abstract class LibraryItem dan subclass Book serta Magazine.
Menerapkan abstract class, inheritance, encapsulation, property, dan polymorphism.
"""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Kelas abstrak yang menjadi dasar seluruh item perpustakaan."""

    def __init__(self, item_id: str, judul: str, tahun: int):
        """Menginisialisasi identitas dan status peminjaman item."""
        self._id = item_id
        self._judul = judul
        self.tahun = tahun  # Menggunakan setter agar tervalidasi
        self.__is_dipinjam = False

    @property
    def id(self) -> str:
        """Mengembalikan ID item."""
        return self._id

    @property
    def judul(self) -> str:
        """Mengembalikan judul item."""
        return self._judul

    @property
    def tahun(self) -> int:
        """Mengembalikan tahun terbit item."""
        return self._tahun

    @tahun.setter
    def tahun(self, nilai: int) -> None:
        """Setter untuk tahun dengan validasi data (enkapsulasi)."""
        if not isinstance(nilai, int) or nilai <= 0:
            raise ValueError("Tahun terbit harus berupa bilangan bulat positif.")
        self._tahun = nilai

    @property
    def is_dipinjam(self) -> bool:
        """Membaca status peminjaman tanpa mengubah atribut private secara langsung."""
        return self.__is_dipinjam

    def pinjam(self) -> bool:
        """Mengubah status item menjadi dipinjam jika masih tersedia."""
        if self.__is_dipinjam:
            print(f'Item "{self.judul}" sedang dipinjam.')
            return False
        self.__is_dipinjam = True
        print(f'Item "{self.judul}" berhasil dipinjam.')
        return True

    def kembalikan(self) -> bool:
        """Mengubah status item menjadi tersedia kembali."""
        if not self.__is_dipinjam:
            print(f'Item "{self.judul}" tidak sedang dipinjam.')
            return False
        self.__is_dipinjam = False
        print(f'Item "{self.judul}" berhasil dikembalikan.')
        return True

    @abstractmethod
    def get_detail(self) -> str:
        """Method abstrak yang wajib diimplementasikan setiap subclass."""
        pass


class Book(LibraryItem):
    """Merepresentasikan buku yang menjadi koleksi perpustakaan."""

    def __init__(self, item_id: str, judul: str, tahun: int,
                 penulis: str, jumlah_halaman: int):
        """Menginisialisasi data umum buku dan data khusus buku."""
        super().__init__(item_id, judul, tahun)
        self._penulis = penulis
        self._jumlah_halaman = jumlah_halaman

    def get_detail(self) -> str:
        """Menghasilkan detail buku."""
        return (
            f"[BUKU] ID: {self.id} | Judul: {self.judul} | "
            f"Penulis: {self._penulis} | Tahun: {self.tahun} | "
            f"Halaman: {self._jumlah_halaman}"
        )


class Magazine(LibraryItem):
    """Merepresentasikan majalah yang menjadi koleksi perpustakaan."""

    def __init__(self, item_id: str, judul: str, tahun: int,
                 edisi: str, penerbit: str):
        """Menginisialisasi data umum majalah dan data khusus majalah."""
        super().__init__(item_id, judul, tahun)
        self._edisi = edisi
        self._penerbit = penerbit

    def get_detail(self) -> str:
        """Menghasilkan detail majalah."""
        return (
            f"[MAJALAH] ID: {self.id} | Judul: {self.judul} | "
            f"Edisi: {self._edisi} | Penerbit: {self._penerbit} | "
            f"Tahun: {self.tahun}"
        )
