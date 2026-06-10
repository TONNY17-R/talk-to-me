import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { ThemeContext } from '../../contexts/ThemeContext';
import './Navbar.css';

export const Navbar = ({ user, onLogout }) => {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const { isDarkMode, toggleTheme } = useContext(ThemeContext);

  // better: import ThemeContext at top
  // but to avoid repeating code here, adjust import line above accordingly

  return (
    <nav className="navbar">
      <div className="navbar-flag-strip" aria-hidden="true">
        <span className="navbar-flag stripe-black" />
        <span className="navbar-flag stripe-yellow" />
        <span className="navbar-flag stripe-red" />
      </div>
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <img src="log.PNG" alt="Talk to Me Logo" className="navbar-logo" />
          Talk to Me
          <span>Care • Calm</span>
        </Link>
        <button
          className="hamburger"
          aria-label="Toggle navigation"
          onClick={() => setMenuOpen((o) => !o)}
        >
          ☰
        </button>
        <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
          <Link to="/chat" onClick={() => setMenuOpen(false)}>
            Chat
          </Link>
          <Link to="/assessment" onClick={() => setMenuOpen(false)}>
            Assessments
          </Link>
          <Link to="/counselling" onClick={() => setMenuOpen(false)}>
            Counselling
          </Link>
          <Link to="/resources" onClick={() => setMenuOpen(false)}>
            Resources
          </Link>
        </div>
        <div className="navbar-controls">
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {isDarkMode ? '🌞' : '🌙'}
          </button>
          <div className="navbar-user">
            {user && (
              <>
                <span>{user.name}</span>
                <button onClick={onLogout}>Logout</button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
