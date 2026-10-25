import PropTypes from 'prop-types';
import { NavLink, Route, Routes } from 'react-router-dom';
import Home from './pages/Home/Home.jsx';
import Stats from './pages/Stats/Stats.jsx';

function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink to="/" className="brand" aria-label="PetalPages beranda">
          <span className="brand-icon">♡</span>
          <span>PetalPages<small>Organize Your Reading Journey</small></span>
        </NavLink>
        <nav className="nav-links" aria-label="Navigasi utama">
          <NavLink to="/" end>Perpustakaan</NavLink>
          <NavLink to="/stats">Statistik</NavLink>
        </nav>
      </header>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
      <footer className="footer">Pina Ramanda_124140170</footer>
    </div>
  );
}
App.propTypes = {};
export default App;