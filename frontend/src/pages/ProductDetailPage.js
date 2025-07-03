import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import './ProductDetailPage.css';

const ProductDetailPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/products/${id}/`);
        setProduct(response.data);
      } catch (err) {
        setError('Product not found');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'ANIMAL': '🐻',
      'DOLL': '👧',
      'CHARACTER': '🦄',
      'ACCESSORIES': '🧶',
      'SEASONAL': '🎄'
    };
    return icons[category] || '🧸';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="product-detail-page">
        <div className="container">
          <div className="loading">Loading product details...</div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="product-detail-page">
        <div className="container">
          <div className="error-container">
            <div className="error-icon">😔</div>
            <h2>Product Not Found</h2>
            <p>The product you're looking for doesn't exist or has been removed.</p>
            <Link to="/products" className="btn btn-primary">
              Back to Products
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="product-detail-page">
      <div className="container">
        <nav className="breadcrumb">
          <Link to="/" className="breadcrumb-link">Home</Link>
          <span className="breadcrumb-separator">›</span>
          <Link to="/products" className="breadcrumb-link">Products</Link>
          <span className="breadcrumb-separator">›</span>
          <span className="breadcrumb-current">{product.name}</span>
        </nav>

        <div className="product-detail">
          <div className="product-image-section">
            <div className="product-image-container">
              <img 
                src={product.image} 
                alt={product.name}
                className="product-image"
              />
              {product.is_featured && (
                <span className="featured-badge">⭐ Featured</span>
              )}
            </div>
          </div>

          <div className="product-info-section">
            <div className="product-category">
              <span className="category-icon">{getCategoryIcon(product.category)}</span>
              <span className="category-name">{product.category.toLowerCase()}</span>
            </div>

            <h1 className="product-title">{product.name}</h1>

            <div className="product-price">
              {formatPrice(product.price)}
            </div>

            <div className="product-description">
              <h3>Description</h3>
              <p>{product.description}</p>
            </div>

            <div className="product-features">
              <h3>Features</h3>
              <ul className="features-list">
                <li>
                  <span className="feature-icon">🧶</span>
                  <span>Handcrafted with premium materials</span>
                </li>
                <li>
                  <span className="feature-icon">❤️</span>
                  <span>Made with love and attention to detail</span>
                </li>
                <li>
                  <span className="feature-icon">🎨</span>
                  <span>Unique design and colors</span>
                </li>
                <li>
                  <span className="feature-icon">🛡️</span>
                  <span>Safe and durable materials</span>
                </li>
              </ul>
            </div>

            <div className="product-actions">
              <button className="btn btn-primary btn-large">
                Contact for Purchase
              </button>
              <button className="btn btn-secondary">
                ❤️ Add to Wishlist
              </button>
            </div>

            <div className="product-meta">
              <div className="meta-item">
                <span className="meta-label">Category:</span>
                <Link 
                  to={`/category/${product.category.toLowerCase()}`}
                  className="meta-value category-link"
                >
                  {getCategoryIcon(product.category)} {product.category.toLowerCase()}
                </Link>
              </div>
              <div className="meta-item">
                <span className="meta-label">Added:</span>
                <span className="meta-value">{formatDate(product.created_at)}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Status:</span>
                <span className={`meta-value status ${product.is_available ? 'available' : 'unavailable'}`}>
                  {product.is_available ? '✅ Available' : '❌ Out of Stock'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="back-to-products">
          <Link to="/products" className="btn btn-secondary">
            ← Back to All Products
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
