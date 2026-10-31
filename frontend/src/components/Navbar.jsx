import { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const closeMenu = () => setMenuOpen(false);

  return (
    <>
      <header className="navbar">
        {/* Logo */}
        <Link className="logo" to="/" onClick={closeMenu} aria-label="GreenCart home">
          <span className="logo-leaf" aria-hidden="true">🌿</span>
          GreenCart
        </Link>

        {/* Desktop nav links */}
        <nav className="nav-links" aria-label="Main navigation">
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/products">Products</NavLink>
          <NavLink to="/compare">Compare</NavLink>
          <NavLink to="/about">About</NavLink>
        </nav>

        {/* Desktop CTA */}
        <div className="nav-right">
          <Link className="nav-cta" to="/products">
            Shop now ↗
          </Link>

          {/* Mobile hamburger */}
          <button
            className={`nav-hamburger${menuOpen ? " open" : ""}`}
            onClick={() => setMenuOpen((o) => !o)}
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            aria-label={menuOpen ? "Close menu" : "Open menu"}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </header>

      {/* Mobile slide-down menu */}
      <nav
        id="mobile-menu"
        className={`nav-mobile-menu${menuOpen ? " open" : ""}`}
        aria-label="Mobile navigation"
        aria-hidden={!menuOpen}
      >
        <NavLink to="/" end onClick={closeMenu}>Home</NavLink>
        <NavLink to="/products" onClick={closeMenu}>Products</NavLink>
        <NavLink to="/compare" onClick={closeMenu}>Compare</NavLink>
        <NavLink to="/about" onClick={closeMenu}>About</NavLink>
        <div className="nav-mobile-cta">
          <Link className="primary-button" to="/products" onClick={closeMenu}>
            Shop now ↗
          </Link>
        </div>
      </nav>
    </>
  );
}

export default Navbar;