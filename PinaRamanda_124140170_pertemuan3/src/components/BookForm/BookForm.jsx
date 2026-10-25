import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

const emptyForm = { title: '', author: '', status: 'baca' };

function BookForm({ onSubmit, editingBook, onCancel }) {
  const [form, setForm] = useState(emptyForm);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    setForm(editingBook ? {
      title: editingBook.title,
      author: editingBook.author,
      status: editingBook.status,
    } : emptyForm);
    setErrors({});
  }, [editingBook]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    if (value.trim()) setErrors((current) => ({ ...current, [name]: '' }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const nextErrors = {};
    if (!form.title.trim()) nextErrors.title = 'Judul buku wajib diisi.';
    if (!form.author.trim()) nextErrors.author = 'Nama penulis wajib diisi.';
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    onSubmit({
      ...(editingBook ? { id: editingBook.id } : {}),
      title: form.title.trim(),
      author: form.author.trim(),
      status: form.status,
    });
    setForm(emptyForm);
  };

  return (
    <section className="panel form-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">{editingBook ? 'UPDATE KOLEKSI' : 'CATAT BUKU BARU'}</p>
          <h2>{editingBook ? 'Edit buku' : 'Tambah buku'}</h2>
        </div>
        <span className="heading-sparkle">✿</span>
      </div>
      <form onSubmit={handleSubmit} noValidate>
        <label htmlFor="book-title">Judul buku</label>
        <input id="book-title" name="title" value={form.title} onChange={handleChange}
          placeholder="Judul buku" aria-invalid={Boolean(errors.title)} aria-describedby={errors.title ? 'title-error' : undefined} />
        {errors.title && <p className="field-error" id="title-error">{errors.title}</p>}

        <label htmlFor="book-author">Penulis</label>
        <input id="book-author" name="author" value={form.author} onChange={handleChange}
          placeholder="Nama penulis" aria-invalid={Boolean(errors.author)} aria-describedby={errors.author ? 'author-error' : undefined} />
        {errors.author && <p className="field-error" id="author-error">{errors.author}</p>}

        <label htmlFor="book-status">Status buku</label>
        <select id="book-status" name="status" value={form.status} onChange={handleChange}>
          <option value="milik">Sudah dimiliki</option>
          <option value="baca">Sedang dibaca</option>
          <option value="beli">Ingin dibeli</option>
        </select>
        <div className="form-actions">
          <button className="button-primary" type="submit">{editingBook ? 'Simpan perubahan' : '+ Simpan buku'}</button>
          {editingBook && <button className="button-quiet" type="button" onClick={onCancel}>Batal</button>}
        </div>
      </form>
    </section>
  );
}
BookForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  editingBook: PropTypes.shape({
    id: PropTypes.string.isRequired, title: PropTypes.string.isRequired,
    author: PropTypes.string.isRequired, status: PropTypes.oneOf(['milik', 'baca', 'beli']).isRequired,
  }),
  onCancel: PropTypes.func.isRequired,
};
BookForm.defaultProps = { editingBook: null };
export default BookForm;