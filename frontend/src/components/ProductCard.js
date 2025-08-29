import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  
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

  // Get current image from the images array
  const getCurrentImage = () => {
    if (!product.images || product.images.length === 0) {
      return null;
    }
    return product.images[currentImageIndex];
  };

  // Navigate to previous image
  const goToPreviousImage = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (product.images && product.images.length > 1) {
      setCurrentImageIndex((prevIndex) => 
        prevIndex === 0 ? product.images.length - 1 : prevIndex - 1
      );
    }
  };

  // Navigate to next image
  const goToNextImage = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (product.images && product.images.length > 1) {
      setCurrentImageIndex((prevIndex) => 
        prevIndex === product.images.length - 1 ? 0 : prevIndex + 1
      );
    }
  };

  // Handle image load and adjust fit based on aspect ratio
  const handleImageLoad = (e) => {
    const img = e.target;
    const imageAspectRatio = img.naturalWidth / img.naturalHeight;
    
    // Debug logging
    console.log(`Image: ${img.alt}, Aspect Ratio: ${imageAspectRatio.toFixed(2)}, Natural Size: ${img.naturalWidth}x${img.naturalHeight}`);
    
    // Remove existing aspect ratio classes
    img.classList.remove('landscape', 'portrait', 'square');
    
    // Add appropriate class based on aspect ratio
    // More aggressive thresholds to handle problematic images
    if (imageAspectRatio > 1.1) {
      // Any image wider than 1.1:1 ratio gets cover treatment
      img.classList.add('landscape');
      console.log(`Applied landscape class to: ${img.alt}`);
    } else if (imageAspectRatio < 0.9) {
      // Tall images get contain treatment
      img.classList.add('portrait');
      console.log(`Applied portrait class to: ${img.alt}`);
    } else {
      // Square-ish images get cover treatment for consistency
      img.classList.add('square');
      console.log(`Applied square class to: ${img.alt}`);
    }
  };

  // Handle image load error
  const handleImageError = (e) => {
    console.error('Failed to load image:', e.target.src);
    // You could set a fallback image here if needed
  };

  const currentImage = getCurrentImage();
  const hasMultipleImages = product.images && product.images.length > 1;

  return (
    <div className="product-card">
      <div className="product-image-container">
        {currentImage ? (
          <>
            <img 
              src={currentImage.url} 
              alt={`${product.name} - ${currentImage.filename}`}
              className="product-image"
              loading="lazy"
              onLoad={handleImageLoad}
              onError={handleImageError}
            />
            
            {/* Navigation arrows - only show if multiple images */}
            {hasMultipleImages && (
              <div className="image-navigation">
                <button 
                  className="nav-button nav-left" 
                  onClick={goToPreviousImage}
                  aria-label="Previous Image"
                  title="Previous Image"
                >
                  ◀
                </button>
                <button 
                  className="nav-button nav-right" 
                  onClick={goToNextImage}
                  aria-label="Next Image"
                  title="Next Image"
                >
                  ▶
                </button>
              </div>
            )}
            
            {/* Image indicators - only show if multiple images */}
            {hasMultipleImages && (
              <div className="image-indicators">
                {product.images.map((_, index) => (
                  <button
                    key={index}
                    className={`indicator ${index === currentImageIndex ? 'active' : ''}`}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      setCurrentImageIndex(index);
                    }}
                    aria-label={`Go to image ${index + 1}`}
                  />
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="no-image-placeholder">
            <span className="no-image-icon">🖼️</span>
            <span className="no-image-text">No Image Available</span>
          </div>
        )}
        
        {product.is_featured && (
          <span className="featured-badge">⭐ Featured</span>
        )}
        
        {currentImage && currentImage.is_default && (
          <span className="default-image-badge">📷 Default</span>
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
        
        {/* Image count badge */}
        {hasMultipleImages && (
          <div className="image-count">
            <span className="count-text">
              {currentImageIndex + 1} of {product.images.length} images
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;
