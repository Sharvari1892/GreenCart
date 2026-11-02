import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import { useState } from "react";
import { CartProvider } from "./context/CartContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Products from "./pages/Products";
import Replacements from "./pages/Replacements";
import Compare from "./pages/Compare";
import About from "./pages/About";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import OrderConfirmation from "./pages/OrderConfirmation";
import "./App.css";

function Footer() {
  return (
    <footer className="site-footer" aria-label="Site footer">
      <div className="footer-inner">
        {/* Brand column */}
        <div className="footer-brand">
          <Link className="logo" to="/" aria-label="GreenCart home">
            <span className="logo-leaf" aria-hidden="true">🌿</span>
            GreenCart
          </Link>
          <p>
            Thoughtful shopping for a greener tomorrow. Discover, compare, and
            choose products that are kinder to our planet.
          </p>
          <p className="footer-demo-note">
            ⚠️ Demo site — 15 Indian brands, in-memory database. Data resets on server restart.
          </p>
        </div>

        {/* Shop column */}
        <div className="footer-col">
          <h4>Shop</h4>
          <Link to="/products">All Products</Link>
          <Link to="/cart">My Cart</Link>
          <Link to="/replacements">Find Alternatives</Link>
          <Link to="/compare">Compare</Link>
        </div>

        {/* Company column */}
        <div className="footer-col">
          <h4>Company</h4>
          <Link to="/about">About GreenCart</Link>
        </div>

        {/* Sustainability column */}
        <div className="footer-col">
          <h4>Our approach</h4>
          <Link to="/about">Eco scoring</Link>
          <Link to="/about">How it works</Link>
        </div>
      </div>

      <div className="footer-bottom">
        <span>© 2026 GreenCart. All rights reserved.</span>
        <span>Made with 🌿 for a greener planet.</span>
      </div>
    </footer>
  );
}

function App() {
  const [selectedProducts, setSelectedProducts] = useState([]);

  return (
    <BrowserRouter>
      <CartProvider>
        <div className="app">
          <Navbar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route
              path="/products"
              element={
                <Products
                  selectedProducts={selectedProducts}
                  setSelectedProducts={setSelectedProducts}
                />
              }
            />
            <Route
              path="/replacements"
              element={
                <Replacements
                  selectedProducts={selectedProducts}
                  setSelectedProducts={setSelectedProducts}
                />
              }
            />
            <Route
              path="/compare"
              element={
                <Compare
                  selectedProducts={selectedProducts}
                  setSelectedProducts={setSelectedProducts}
                />
              }
            />
            <Route path="/about" element={<About />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/order-confirmation/:orderId" element={<OrderConfirmation />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>

          <Footer />
        </div>
      </CartProvider>
    </BrowserRouter>
  );
}

export default App;
