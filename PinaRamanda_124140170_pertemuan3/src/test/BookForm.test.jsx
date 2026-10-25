import { describe, it, expect, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import BookForm from '../components/BookForm/BookForm.jsx';

describe('BookForm', () => {
  it('menampilkan input judul, penulis, dan status', () => {
    render(<BookForm onSubmit={vi.fn()} onCancel={vi.fn()} />);
    expect(screen.getByLabelText(/judul buku/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/penulis/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status buku/i)).toBeInTheDocument();
  });

  it('menampilkan error saat judul dan penulis kosong', () => {
    render(<BookForm onSubmit={vi.fn()} onCancel={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /simpan buku/i }));
    expect(screen.getByText('Judul buku wajib diisi.')).toBeInTheDocument();
    expect(screen.getByText('Nama penulis wajib diisi.')).toBeInTheDocument();
  });

  it('mengirim data buku yang valid', () => {
    const onSubmit = vi.fn();
    render(<BookForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    fireEvent.change(screen.getByLabelText(/judul buku/i), { target: { value: 'Laut Bercerita' } });
    fireEvent.change(screen.getByLabelText(/penulis/i), { target: { value: 'Leila S. Chudori' } });
    fireEvent.click(screen.getByRole('button', { name: /simpan buku/i }));
    expect(onSubmit).toHaveBeenCalledWith({ title: 'Laut Bercerita', author: 'Leila S. Chudori', status: 'baca' });
  });
});