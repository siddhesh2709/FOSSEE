import React from 'react';
import './Navbar.css';

function Navbar({ activeTab, setActiveTab }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="brand-icon">⚗️</span>
          <span className="brand-name">Chemical Equipment Visualizer</span>
        </div>
        
        <ul className="navbar-menu">
          <li 
            className={`nav-item ${activeTab === 'home' ? 'active' : ''}`}
            onClick={() => setActiveTab('home')}
          >
            <span className="nav-icon">🏠</span>
            Home
          </li>
          <li 
            className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <span className="nav-icon">📊</span>
            History
          </li>
          <li 
            className={`nav-item ${activeTab === 'downloads' ? 'active' : ''}`}
            onClick={() => setActiveTab('downloads')}
          >
            <span className="nav-icon">📥</span>
            Downloads
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
