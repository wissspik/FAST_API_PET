import React from 'react';
import './Dashboard.css';

// Заглушки для товаров (пример)
const products = [
  { id: 1, name: 'Product 1', price: '199₽', img: '🟦', category: 'Tech' },
  { id: 2, name: 'Product 2', price: '299₽', img: '🟥', category: 'Books' },
  { id: 3, name: 'Product 3', price: '399₽', img: '🟩', category: 'Sneakers' },
  { id: 4, name: 'Product 4', price: '499₽', img: '🟨', category: 'Travel' },
];

// Пустые блоки для категорий (будут заменены на реальные данные)
const categoryPlaceholders = Array(6).fill(null);

const Dashboard = () => {
  const handleLogout = () => {
    // Здесь будет логика выхода
    console.log('Logout clicked');
  };

  return (
    <div className="dashboard-main">
      <header className="dashboard-header">
        <div className="logo">Shopcart</div>
        <nav className="main-nav">
          <a href="#" className="nav-link">Home</a>
          <a href="#" className="nav-link">Categories</a>
          <a href="#" className="nav-link">Deals</a>
          <a href="#" className="nav-link">Delivery</a>
          <div className="search-container">
            <input type="text" placeholder="Search Product" className="search-input" />
            <button className="search-button">🔍</button>
          </div>
        </nav>
        <div className="user-actions">
          <span className="user-icon" title="Личный кабинет">👤</span>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <section className="dashboard-categories">
        <h2 className="section-title">Categories</h2>
        <div className="categories-list">
          {categoryPlaceholders.map((_, idx) => (
            <div className="category-card placeholder" key={idx} />
          ))}
        </div>
      </section>

      <section className="dashboard-products">
        <h2 className="section-title">Products</h2>
        <div className="products-list">
          {products.map(product => (
            <div className="product-card" key={product.id}>
              <div className="product-img">{product.img}</div>
              <div className="product-info">
                <div className="product-name">{product.name}</div>
                <div className="product-price">{product.price}</div>
                <button className="add-to-cart-button">Add to Cart</button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Dashboard; 