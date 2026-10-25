import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { useBooks } from '../../context/BookContext.jsx';
import useBookStats from '../../hooks/useBookStats.js';

function Stats() {
  const { books } = useBooks();
  const stats = useBookStats(books);
  const data = [
    { label: 'Sudah dimiliki', key: 'owned', color: 'bar-owned', emoji: '♡' },
    { label: 'Sedang dibaca', key: 'reading', color: 'bar-reading', emoji: '◷' },
    { label: 'Ingin dibeli', key: 'wishlist', color: 'bar-wishlist', emoji: '☆' },
  ];
  return (
    <section className="stats-page">
      <div className="page-intro"><p className="eyebrow">SEDIKIT MELIHAT PROGRES</p><h1>Statistik <span>bacaanmu.</span></h1><p>Kenali isi rak bukumu dan rencanakan petualangan membaca selanjutnya.</p></div>
      <div className="big-total panel"><span className="big-total-icon">▤</span><div><small>Seluruh koleksi</small><strong>{stats.total} <span>buku</span></strong></div><span className="total-decoration">✿</span></div>
      <div className="stats-detail panel">
        <h2>Ringkasan koleksi</h2>
        {data.map((item) => {
          const count = stats[item.key];
          const percent = stats.total ? Math.round((count / stats.total) * 100) : 0;
          return <div className="progress-item" key={item.key}>
            <div className="progress-label"><span>{item.emoji} &nbsp;{item.label}</span><strong>{count} <small>({percent}%)</small></strong></div>
            <div className="progress-track"><div className={`progress-fill ${item.color}`} style={{ width: `${percent}%` }} /></div>
          </div>;
        })}
      </div>
      <Link className="button-primary back-link" to="/">← Kembali ke perpustakaan</Link>
    </section>
  );
}
Stats.propTypes = {};
export default Stats;