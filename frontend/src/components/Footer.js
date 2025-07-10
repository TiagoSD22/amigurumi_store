import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">
              <span className="footer-icon">🧶</span>
              Amigurumi Store
            </h3>
            <p className="footer-description">
              Handcrafted amigurumi toys made with love and care. Each piece is unique and created with the finest materials.
            </p>
            <div className="social-links">
              <button type="button" className="social-link" aria-label="Facebook">📘</button>
              <button type="button" className="social-link" aria-label="Instagram">📷</button>
              <button type="button" className="social-link" aria-label="Twitter">🐦</button>
            </div>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Categories</h4>
            <ul className="footer-links">
              <li><a href="/category/animal">Animals</a></li>
              <li><a href="/category/doll">Dolls</a></li>
              <li><a href="/category/character">Characters</a></li>
              <li><a href="/category/accessories">Accessories</a></li>
              <li><a href="/category/seasonal">Seasonal</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Customer Service</h4>
            <ul className="footer-links">
              <li><button type="button" className="footer-link-btn">Contact Us</button></li>
              <li><button type="button" className="footer-link-btn">Shipping Info</button></li>
              <li><button type="button" className="footer-link-btn">Returns</button></li>
              <li><button type="button" className="footer-link-btn">FAQ</button></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Contact Info</h4>
            <div className="contact-info">
              <p>📧 hello@amigurumistore.com</p>
              <p>📞 +1 (555) 123-4567</p>
              <p>📍 123 Craft Street, Artisan City, AC 12345</p>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2024 Amigurumi Store. All rights reserved. Made with ❤️ for craft lovers.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
