import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import api from '../services/api';
import './HomePage.css';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        setLoading(true);
        const response = await api.get('/products/featured/');
        setFeaturedProducts(response.data);
      } catch (err) {
        setError('Failed to load featured products');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedProducts();
  }, []);

  const categories = [
    {
      id: 'animal',
      name: 'Animals',
      icon: '🐻',
      description: 'Cute and cuddly animal friends'
    },
    {
      id: 'doll',
      name: 'Dolls',
      icon: '👧',
      description: 'Beautiful handmade dolls'
    },
    {
      id: 'character',
      name: 'Characters',
      icon: '🦄',
      description: 'Fantasy and cartoon characters'
    },
    {
      id: 'accessories',
      name: 'Accessories',
      icon: '🧶',
      description: 'Useful and decorative items'
    },
    {
      id: 'seasonal',
      name: 'Seasonal',
      icon: '🎄',
      description: 'Holiday and seasonal decorations'
    }
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>Handcrafted Amigurumi</h1>
          <p>Discover our collection of beautiful, handmade amigurumi toys and accessories, each created with love and attention to detail.</p>
          <Link to="/products" className="btn btn-primary hero-btn">
            Shop Now
          </Link>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="section featured-products">
        <div className="container">
          <h2 className="section-title">Featured Products</h2>
          <p className="section-subtitle">
            Check out our most popular and recently added amigurumi creations
          </p>
          
          {loading && <div className="loading">Loading featured products...</div>}
          {error && <div className="error">{error}</div>}
          
          {!loading && !error && (
            <div className="products-grid grid grid-4">
              {featuredProducts.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
          
          {!loading && !error && featuredProducts.length === 0 && (
            <div className="no-products">
              <p>No featured products available at the moment.</p>
            </div>
          )}
          
          <div className="text-center mt-4">
            <Link to="/products" className="btn btn-secondary">
              View All Products
            </Link>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="section categories">
        <div className="container">
          <h2 className="section-title">Shop by Category</h2>
          <p className="section-subtitle">
            Find the perfect amigurumi for every occasion and taste
          </p>
          
          <div className="category-grid">
            {categories.map(category => (
              <Link
                key={category.id}
                to={`/category/${category.id}`}
                className="category-card"
              >
                <div className="category-icon">{category.icon}</div>
                <h3 className="category-title">{category.name}</h3>
                <p className="category-description">{category.description}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="section about-section">
        <div className="container">
          <div className="about-content">
            <div className="about-text">
              <h2 className="section-title">About Our Craft</h2>
              <p>
                Every amigurumi in our store is lovingly handcrafted using the finest materials and traditional techniques. 
                We believe in creating not just toys, but cherished companions that bring joy and comfort to people of all ages.
              </p>
              <p>
                Our artisans put their heart into every stitch, ensuring that each piece is unique and made to last. 
                From adorable animals to whimsical characters, our collection celebrates the art of amigurumi.
              </p>
              <div className="features">
                <div className="feature">
                  <span className="feature-icon">🧶</span>
                  <span>Premium Materials</span>
                </div>
                <div className="feature">
                  <span className="feature-icon">❤️</span>
                  <span>Made with Love</span>
                </div>
                <div className="feature">
                  <span className="feature-icon">🎨</span>
                  <span>Unique Designs</span>
                </div>
              </div>
            </div>
            <div className="about-image">
              <div className="craft-illustration">
                <span>🧶</span>
                <span>✂️</span>
                <span>🪡</span>
                <span>❤️</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
