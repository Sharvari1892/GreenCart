import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Products from "./pages/Products";
import Compare from "./pages/Compare";
import About from "./pages/About";
import "./App.css";

function App() {
  const [selectedProducts, setSelectedProducts] = useState([]);

  return (
    <BrowserRouter>
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
            path="/compare"
            element={
              <Compare
                selectedProducts={selectedProducts}
                setSelectedProducts={setSelectedProducts}
              />
            }
          />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        <footer className="site-footer">
          <a className="logo" href="/">🌿 GreenCart</a>
          <p>Thoughtful shopping for a greener tomorrow.</p>
          <span>© 2026 GreenCart</span>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;