import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const categories = [
    { id: 'animal', name: 'Animals', icon: '🐻' },
    { id: 'doll', name: 'Dolls', icon: '👧' },
    { id: 'character', name: 'Characters', icon: '🦄' },
    { id: 'accessories', name: 'Accessories', icon: '🧶' },
    { id: 'seasonal', name: 'Seasonal', icon: '🎄' },
  ];

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link to="/" className="logo">
            <span className="logo-icon">🧶</span>
            <span className="logo-text">Amigurumi Store</span>
          </Link>
          
          <nav className={`nav ${isMenuOpen ? 'nav-open' : ''}`}>
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/products" className="nav-link">All Products</Link>
            <div className="dropdown">
              <span className="nav-link dropdown-toggle">Categories</span>
              <div className="dropdown-menu">
                {categories.map(category => (
                  <Link
                    key={category.id}
                    to={`/category/${category.id}`}
                    className="dropdown-item"
                  >
                    <span className="category-icon">{category.icon}</span>
                    {category.name}
                  </Link>
                ))}
              </div>
            </div>
          </nav>

          <div className="header-actions">
            <button className="btn btn-primary">Contact Us</button>
            <button 
              className="mobile-menu-toggle"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
