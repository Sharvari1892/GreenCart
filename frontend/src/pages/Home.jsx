import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import CategoryCard from "../components/CategoryCard";
import ProductCard from "../components/ProductCard";
import heroImg from "../assets/hero_grocery.png";

const API_URL = "http://127.0.0.1:8000/api";

/* ─── Category skeleton placeholders ───────────────────────── */
function CategorySkeleton() {
  return (
    <div className="category-grid" aria-hidden="true">
      {Array.from({ length: 6 }, (_, i) => (
        <div key={i} className="category-card" style={{ cursor: "default", pointerEvents: "none" }}>
          <div className="skeleton category-icon" style={{ borderRadius: "var(--radius-lg)" }} />
          <div className="skeleton skeleton-line w-60" style={{ height: 14, marginTop: 4 }} />
          <div className="skeleton skeleton-line w-80" style={{ height: 10 }} />
        </div>
      ))}
    </div>
  );
}

/* ─── Small product card skeleton ───────────────────────────── */
function FeaturedSkeleton() {
  return (
    <div className="product-grid" aria-hidden="true">
      {Array.from({ length: 3 }, (_, i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton skeleton-img" />
          <div className="skeleton-body">
            <div className="skeleton skeleton-line w-40" />
            <div className="skeleton skeleton-line w-80 h-20" />
            <div className="skeleton skeleton-line w-60" />
            <div className="skeleton skeleton-line w-100" />
          </div>
        </div>
      ))}
    </div>
  );
}

function Home() {
  const navigate = useNavigate();

  /* categories */
  const [categories, setCategories]         = useState([]);
  const [catsLoading, setCatsLoading]       = useState(true);
  const [catsError, setCatsError]           = useState("");

  /* featured products */
  const [featured, setFeatured]             = useState([]);
  const [featuredLoading, setFeaturedLoading] = useState(true);
  const [featuredError, setFeaturedError]   = useState("");

  /* category map for ProductCard */
  const [categoryMap, setCategoryMap]       = useState(new Map());

  /* compare toggle on home page just sends user to Products to pick items */

  useEffect(() => {
    const controller = new AbortController();

    async function fetchAll() {
      /* ── Categories ── */
      try {
        const res = await fetch(`${API_URL}/categories`, { signal: controller.signal });
        if (res.ok) {
          const data = await res.json();
          setCategories(Array.isArray(data) ? data : []);
          const map = new Map((Array.isArray(data) ? data : []).map((c) => [c.id, c.name]));
          setCategoryMap(map);
        } else {
          setCatsError("Could not load categories.");
        }
      } catch (err) {
        if (err.name !== "AbortError") setCatsError("Could not load categories.");
      } finally {
        if (!controller.signal.aborted) setCatsLoading(false);
      }

      /* ── Featured products (top 6) ── */
      try {
        const res = await fetch(
          `${API_URL}/products?page=1&page_size=6&sort_by=sustainability_score&sort_desc=true`,
          { signal: controller.signal }
        );
        if (res.ok) {
          const data = await res.json();
          setFeatured(data.items || []);
        } else {
          setFeaturedError("Could not load products.");
        }
      } catch (err) {
        if (err.name !== "AbortError") setFeaturedError("Could not load products.");
      } finally {
        if (!controller.signal.aborted) setFeaturedLoading(false);
      }
    }

    fetchAll();
    return () => controller.abort();
  }, []);

  /* Navigate to /products pre-filtered by category id */
  function handleCategorySelect(categoryId) {
    navigate(`/products?category=${categoryId}`);
  }

  /* Minimal compare toggle for the featured section — just navigates to Products */
  function handleToggleCompare(_id) {
    navigate("/products");
  }

  function getCategoryName(product) {
    return categoryMap.get(product.category_id) || product.category?.name || "Product";
  }

  return (
    <main>
      {/* ══════════════════════════════════════════════════
          HERO
          ══════════════════════════════════════════════════ */}
      <section className="hero" aria-label="GreenCart hero">
        <div
          className="hero-bg"
          style={{ backgroundImage: `url(${heroImg})` }}
          aria-hidden="true"
        />
        <div className="hero-overlay" aria-hidden="true" />

        <div className="hero-content">
          <span className="eyebrow">A greener way to shop</span>

          <h1>
            Better choices.<br />
            <em>Greener future.</em>
          </h1>

          <p className="hero-sub">
            Discover everyday products, compare their sustainability
            scores, and make choices that are kinder to our planet —
            all in one place.
          </p>

          <div className="hero-actions">
            <Link className="primary-button" to="/products">
              Explore products ↗
            </Link>
            <Link className="secondary-button" to="/compare">
              Compare products
            </Link>
          </div>

          <div className="hero-stats" aria-label="Key features">
            <div className="hero-stats-item">
              <strong>Thoughtful</strong>
              <small>product discovery</small>
            </div>
            <div className="hero-stats-item">
              <strong>Eco-aware</strong>
              <small>shopping choices</small>
            </div>
            <div className="hero-stats-item">
              <strong>Side-by-side</strong>
              <small>product comparison</small>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════
          BENEFITS BAR
          ══════════════════════════════════════════════════ */}
      <section className="benefits" aria-label="Why GreenCart">
        <div className="benefits-inner">
          <div className="benefit-item">
            <div className="benefit-icon" aria-hidden="true">🌍</div>
            <div className="benefit-text">
              <strong>Planet-conscious</strong>
              <span>Explore greener alternatives</span>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon" aria-hidden="true">⚖️</div>
            <div className="benefit-text">
              <strong>Compare products</strong>
              <span>Make informed decisions</span>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon" aria-hidden="true">🛒</div>
            <div className="benefit-text">
              <strong>Shop smarter</strong>
              <span>Find what fits your needs</span>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════
          CATEGORIES (live from API)
          ══════════════════════════════════════════════════ */}
      <section className="section-wrap section-alt" aria-labelledby="cat-heading">
        <div className="section-header">
          <div className="section-header-text">
            <span className="eyebrow">Browse by category</span>
            <h2 id="cat-heading">Shop your favourites</h2>
            <p>Find products in the categories you care about most.</p>
          </div>
          <Link className="secondary-button" to="/products">
            View all →
          </Link>
        </div>

        {catsLoading ? (
          <CategorySkeleton />
        ) : catsError ? (
          <p style={{ color: "var(--clr-text-muted)", fontSize: 14 }}>{catsError}</p>
        ) : categories.length > 0 ? (
          <div className="category-grid">
            {categories.map((cat) => (
              <CategoryCard
                key={cat.id}
                category={cat}
                onSelect={handleCategorySelect}
              />
            ))}
          </div>
        ) : (
          <p style={{ color: "var(--clr-text-muted)", fontSize: 14 }}>
            No categories available yet.
          </p>
        )}
      </section>

      {/* ══════════════════════════════════════════════════
          FEATURED PRODUCTS (live from API, top 6)
          ══════════════════════════════════════════════════ */}
      <section className="section-wrap" aria-labelledby="featured-heading">
        <div className="section-header">
          <div className="section-header-text">
            <span className="eyebrow">Top picks</span>
            <h2 id="featured-heading">Featured products</h2>
            <p>Highly sustainability-rated products from our catalogue.</p>
          </div>
          <Link className="secondary-button" to="/products">
            View all products →
          </Link>
        </div>

        {featuredLoading ? (
          <FeaturedSkeleton />
        ) : featuredError ? (
          <div className="no-results">
            <div className="no-results-icon">😔</div>
            <h3>Couldn&rsquo;t load products</h3>
            <p>{featuredError}</p>
            <Link className="primary-button" to="/products">
              Browse all products
            </Link>
          </div>
        ) : featured.length > 0 ? (
          <div className="product-grid">
            {featured.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                categoryName={getCategoryName(product)}
                isSelected={false}
                onToggleCompare={handleToggleCompare}
              />
            ))}
          </div>
        ) : (
          <div className="no-results">
            <div className="no-results-icon">🌿</div>
            <h3>No products yet</h3>
            <p>Products will appear here once they are added to the catalogue.</p>
          </div>
        )}
      </section>

      {/* ══════════════════════════════════════════════════
          CTA BANNER
          ══════════════════════════════════════════════════ */}
      <section className="home-cta" aria-label="Call to action">
        <h2>Ready to shop with purpose?</h2>
        <p>
          Explore our full catalogue and compare sustainability scores
          side by side before you choose.
        </p>
        <div className="home-cta-actions">
          <Link className="primary-button" to="/products">
            Browse all products ↗
          </Link>
          <Link className="secondary-button" to="/compare">
            Start comparing
          </Link>
        </div>
      </section>
    </main>
  );
}

export default Home;