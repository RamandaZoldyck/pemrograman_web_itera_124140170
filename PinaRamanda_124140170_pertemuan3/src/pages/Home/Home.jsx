import { useMemo, useState } from 'react';
import PropTypes from 'prop-types';
import { useBooks } from '../../context/BookContext.jsx';
import useBookStats from '../../hooks/useBookStats.js';
import BookForm from '../../components/BookForm/BookForm.jsx';
import BookList from '../../components/BookList/BookList.jsx';
import BookFilter from '../../components/BookFilter/BookFilter.jsx';

function Home() {
  const { books, addBook, updateBook, deleteBook } = useBooks();
  const stats = useBookStats(books);
  const [status, setStatus] = useState('semua');
  const [search, setSearch] = useState('');
  const [editingBook, setEditingBook] = useState(null);

  const filteredBooks = useMemo(() => books.filter((book) => {
    const matchesStatus = status === 'semua' || book.status === status;
    const term = search.toLowerCase().trim();
    const matchesSearch = book.title.toLowerCase().includes(term) || book.author.toLowerCase().includes(term);
    return matchesStatus && matchesSearch;
  }), [books, status, search]);

  const handleSubmit = (book) => {
    if (editingBook) {
      updateBook(book);
      setEditingBook(null);
    } else {
      addBook(book);
    }
  };

  const handleDelete = (id) => {
    if (window.confirm('Yakin ingin menghapus buku ini?')) {
      deleteBook(id);
      if (editingBook?.id === id) setEditingBook(null);
    }
  };

  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">RUANG KECIL, CERITA BESAR</p>
          <h1>Semua bukumu,<br /><span>di satu tempat.</span></h1>
          <p className="hero-description">Simpan daftar bacaan, lacak buku yang sedang kamu nikmati, dan kumpulkan wishlist buku berikutnya.</p>
          <div className="hero-note"><span>✧</span> Satu halaman lagi, satu petualangan baru.</div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="sun-shape" />
          <div className="book-stack stack-back"><span /></div>
          <div className="book-stack stack-mid"><span /></div>
          <div className="book-stack stack-front"><span>read<br />more ♡</span></div>
          <div className="floating-heart">♡</div>
          <div className="floating-star">✦</div>
        </div>
      </section>

      <section className="stats-strip" aria-label="Ringkasan buku">
        <div className="mini-stat"><span className="stat-icon">▤</span><div><strong>{stats.total}</strong><small>Total buku</small></div></div>
        <div className="mini-stat"><span className="stat-icon blush">♡</span><div><strong>{stats.owned}</strong><small>Sudah dimiliki</small></div></div>
        <div className="mini-stat"><span className="stat-icon lilac">◷</span><div><strong>{stats.reading}</strong><small>Sedang dibaca</small></div></div>
        <div className="mini-stat"><span className="stat-icon peach">☆</span><div><strong>{stats.wishlist}</strong><small>Wishlist</small></div></div>
      </section>

      <div className="workspace">
        <BookForm onSubmit={handleSubmit} editingBook={editingBook} onCancel={() => setEditingBook(null)} />
        <section className="library-section">
          <div className="section-heading library-heading">
            <div><p className="eyebrow">KOLEKSI PERSONAL</p><h2>Rak bukuku <span className="count-bubble">{filteredBooks.length}</span></h2></div>
            <span className="tiny-flower">✿</span>
          </div>
          <BookFilter status={status} onStatusChange={setStatus} search={search} onSearchChange={setSearch} />
          <BookList books={filteredBooks} onEdit={setEditingBook} onDelete={handleDelete} />
        </section>
      </div>
    </>
  );
}
Home.propTypes = {};
export default Home;