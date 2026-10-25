import PropTypes from 'prop-types';

function BookFilter({ status, onStatusChange, search, onSearchChange }) {
  return (
    <div className="filter-row">
      <div className="search-wrap">
        <span aria-hidden="true">⌕</span>
        <input aria-label="Cari judul atau penulis" value={search} onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Cari judul atau penulis..." />
      </div>
      <label className="filter-select-label" htmlFor="status-filter">Status
        <select id="status-filter" value={status} onChange={(event) => onStatusChange(event.target.value)}>
          <option value="semua">Semua buku</option>
          <option value="milik">Sudah dimiliki</option>
          <option value="baca">Sedang dibaca</option>
          <option value="beli">Ingin dibeli</option>
        </select>
      </label>
    </div>
  );
}
BookFilter.propTypes = {
  status: PropTypes.oneOf(['semua', 'milik', 'baca', 'beli']).isRequired,
  onStatusChange: PropTypes.func.isRequired,
  search: PropTypes.string.isRequired,
  onSearchChange: PropTypes.func.isRequired,
};
export default BookFilter;