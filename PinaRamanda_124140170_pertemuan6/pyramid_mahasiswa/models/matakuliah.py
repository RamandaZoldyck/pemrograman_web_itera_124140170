from sqlalchemy import CheckConstraint, Column, Integer, String

from .meta import Base


class Matakuliah(Base):
    """Tabel ``matakuliah``."""

    __tablename__ = 'matakuliah'
    __table_args__ = (
        CheckConstraint('sks > 0', name='sks_positif'),
        CheckConstraint('semester > 0', name='semester_positif'),
    )

    id = Column(Integer, primary_key=True)
    kode_mk = Column(String(20), unique=True, nullable=False)
    nama_mk = Column(String(100), nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'kode_mk': self.kode_mk,
            'nama_mk': self.nama_mk,
            'sks': self.sks,
            'semester': self.semester,
        }
