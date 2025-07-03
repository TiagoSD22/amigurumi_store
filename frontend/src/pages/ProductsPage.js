import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import api from '../services/api';
import './ProductsPage.css';

const ProductsPage = () => {
  const { category } = useParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(category || 'all');

  const categories = [
    { id: 'all', name: 'All Products', icon: '🛍️' },
    { id: 'animal', name: 'Animals', icon: '🐻' },
    { id: 'doll', name: 'Dolls', icon: '👧' },
    { id: 'character', name: 'Characters', icon: '🦄' },
    { id: 'accessories', name: 'Accessories', icon: '🧶' },
    { id: 'seasonal', name: 'Seasonal', icon: '🎄' },
  ];

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        let url = '/products/';
        
        if (selectedCategory && selectedCategory !== 'all') {
          url = `/products/category/${selectedCategory}/`;
        }
        
        const response = await api.get(url);
        setProducts(response.data);
      } catch (err) {
        setError('Failed to load products');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [selectedCategory]);

  useEffect(() => {
    if (category) {
      setSelectedCategory(category);
    }
  }, [category]);

  const handleCategoryChange = (newCategory) => {
    setSelectedCategory(newCategory);
  };

  const getCategoryTitle = () => {
    const cat = categories.find(c => c.id === selectedCategory);
    return cat ? cat.name : 'All Products';
  };

  return (
    <div className="products-page">
      <div className="container">
        <div className="page-header">
          <h1 className="page-title">{getCategoryTitle()}</h1>
          <p className="page-subtitle">
            {selectedCategory === 'all' 
              ? 'Discover our complete collection of handcrafted amigurumi'
              : `Beautiful ${getCategoryTitle().toLowerCase()} made with love and care`
            }
          </p>
        </div>

        {/* Category Filter */}
        <div className="category-filter">
          <h3 className="filter-title">Filter by Category</h3>
          <div className="category-buttons">
            {categories.map(cat => (
              <button
                key={cat.id}
                className={`category-btn ${selectedCategory === cat.id ? 'active' : ''}`}
                onClick={() => handleCategoryChange(cat.id)}
              >
                <span className="category-icon">{cat.icon}</span>
                <span className="category-name">{cat.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Products Grid */}
        <div className="products-section">
          {loading && <div className="loading">Loading products...</div>}
          {error && <div className="error">{error}</div>}
          
          {!loading && !error && (
            <>
              <div className="products-info">
                <p className="products-count">
                  {products.length} {products.length === 1 ? 'product' : 'products'} found
                </p>
              </div>
              
              <div className="products-grid grid grid-4">
                {products.map(product => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </>
          )}
          
          {!loading && !error && products.length === 0 && (
            <div className="no-products">
              <div className="no-products-icon">😔</div>
              <h3>No products found</h3>
              <p>
                {selectedCategory === 'all' 
                  ? 'We don\'t have any products available at the moment.'
                  : `No products found in the ${getCategoryTitle().toLowerCase()} category.`
                }
              </p>
              <button 
                className="btn btn-primary"
                onClick={() => handleCategoryChange('all')}
              >
                View All Products
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;
