import React from 'react';
import { Link } from 'react-router-dom';
import './ProductCard.css';

const ProductCard = ({ product }) => {
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

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img 
          src={product.image} 
          alt={product.name}
          className="product-image"
          loading="lazy"
        />
        {product.is_featured && (
          <span className="featured-badge">⭐ Featured</span>
        )}
      </div>
      
      <div className="product-info">
        <div className="product-category">
          <span className="category-icon">{getCategoryIcon(product.category)}</span>
          <span className="category-name">{product.category.toLowerCase()}</span>
        </div>
        
        <h3 className="product-name">{product.name}</h3>
        
        <p className="product-description">
          {product.description.length > 100 
            ? `${product.description.substring(0, 100)}...` 
            : product.description}
        </p>
        
        <div className="product-footer">
          <span className="product-price">{formatPrice(product.price)}</span>
          <Link 
            to={`/products/${product.id}`} 
            className="btn btn-primary btn-sm"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
