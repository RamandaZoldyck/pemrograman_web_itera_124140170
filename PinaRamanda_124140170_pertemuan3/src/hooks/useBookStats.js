import { useMemo } from 'react';

// Menghitung ringkasan koleksi buku tanpa mengubah data aslinya.
export default function useBookStats(books) {
  return useMemo(() => ({
    total: books.length,
    owned: books.filter((book) => book.status === 'milik').length,
    reading: books.filter((book) => book.status === 'baca').length,
    wishlist: books.filter((book) => book.status === 'beli').length,
  }), [books]);
}