import { NavLink, Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <header className="navbar">
      <Link className="logo" to="/">
        <span className="logo-icon">🌿</span>
        GreenCart
      </Link>

      <nav className="nav-links" aria-label="Main navigation">
        <NavLink to="/" end>Home</NavLink>
        <NavLink to="/products">Products</NavLink>
        <NavLink to="/compare">Compare</NavLink>
        <NavLink to="/about">About</NavLink>
      </nav>

      <Link className="nav-cta" to="/products">
        Explore products ↗
      </Link>
    </header>
  );
}

export default Navbar;