import PropTypes from 'prop-types';

const statusLabels = { milik: 'Sudah dimiliki', baca: 'Sedang dibaca', beli: 'Ingin dibeli' };

function BookList({ books, onEdit, onDelete }) {
  if (!books.length) {
    return <div className="empty-state"><span>♡</span><h3>Belum ada buku di sini</h3></div>;
  }

  return (
    <div className="book-grid">
      {books.map((book) => (
        <article className="book-card" key={book.id}>
          <div className={`book-cover cover-${book.status}`} aria-hidden="true">
            <span className="cover-heart">♡</span><span className="cover-lines" />
          </div>
          <div className="book-info">
            <span className={`status-pill status-${book.status}`}>{statusLabels[book.status]}</span>
            <h3>{book.title}</h3>
            <p className="book-author">oleh {book.author}</p>
            <div className="book-actions">
              <button type="button" className="button-small" onClick={() => onEdit(book)} aria-label={`Edit ${book.title}`}>Edit</button>
              <button type="button" className="button-small danger" onClick={() => onDelete(book.id)} aria-label={`Hapus ${book.title}`}>Hapus</button>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
BookList.propTypes = {
  books: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired, title: PropTypes.string.isRequired,
    author: PropTypes.string.isRequired, status: PropTypes.oneOf(['milik', 'baca', 'beli']).isRequired,
  })).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
};
export default BookList;