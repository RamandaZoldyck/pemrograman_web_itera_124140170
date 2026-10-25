import { describe, it, expect, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import BookList from '../components/BookList/BookList.jsx';

const books = [{ id: '1', title: 'Bumi', author: 'Tere Liye', status: 'milik' }];

describe('BookList', () => {
  it('menampilkan judul, penulis, dan status buku', () => {
    render(<BookList books={books} onEdit={vi.fn()} onDelete={vi.fn()} />);
    expect(screen.getByText('Bumi')).toBeInTheDocument();
    expect(screen.getByText('oleh Tere Liye')).toBeInTheDocument();
    expect(screen.getByText('Sudah dimiliki')).toBeInTheDocument();
  });

  it('memanggil fungsi edit saat tombol edit diklik', () => {
    const onEdit = vi.fn();
    render(<BookList books={books} onEdit={onEdit} onDelete={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Edit Bumi' }));
    expect(onEdit).toHaveBeenCalledWith(books[0]);
  });

  it('menampilkan empty state saat tidak ada buku', () => {
    render(<BookList books={[]} onEdit={vi.fn()} onDelete={vi.fn()} />);
    expect(screen.getByText('Belum ada buku di sini')).toBeInTheDocument();
  });
});