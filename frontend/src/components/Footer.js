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
              <a href="#" className="social-link">📘</a>
              <a href="#" className="social-link">📷</a>
              <a href="#" className="social-link">🐦</a>
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
              <li><a href="#contact">Contact Us</a></li>
              <li><a href="#shipping">Shipping Info</a></li>
              <li><a href="#returns">Returns</a></li>
              <li><a href="#faq">FAQ</a></li>
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
