from sqlalchemy import Column, Date, Integer, String, Text

from .meta import Base


class Mahasiswa(Base):
    """Tabel ``mahasiswa``."""

    __tablename__ = 'mahasiswa'

    id = Column(Integer, primary_key=True)
    nim = Column(String(20), unique=True, nullable=False)
    nama = Column(String(100), nullable=False)
    jurusan = Column(String(100), nullable=False)
    tanggal_lahir = Column(Date, nullable=True)
    alamat = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nim': self.nim,
            'nama': self.nama,
            'jurusan': self.jurusan,
            'tanggal_lahir': (
                self.tanggal_lahir.isoformat() if self.tanggal_lahir else None
            ),
            'alamat': self.alamat,
        }
