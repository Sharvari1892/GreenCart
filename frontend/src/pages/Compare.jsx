import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import OnlineBrandCompare from "../components/OnlineBrandCompare";

const API_URL = "http://127.0.0.1:8000/api";

function Compare({ selectedProducts = [], setSelectedProducts }) {
  const [activeTab, setActiveTab] = useState("online"); // "online" or "catalog"
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function fetchProducts() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_URL}/products?page=1&page_size=100`);
        if (!response.ok) throw new Error("Could not load products from the server.");

        const data = await response.json();
        const items = Array.isArray(data) ? data : data.items || [];
        if (!cancelled) setProducts(items);
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load products.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchProducts();
    return () => {
      cancelled = true;
    };
  }, []);

  /* Products currently being compared in catalog mode */
  const compared = useMemo(() => {
    const ids = selectedProducts.map(Number);
    return products.filter((p) => ids.includes(Number(p.id)));
  }, [products, selectedProducts]);

  function removeProduct(id) {
    setSelectedProducts((current) =>
      current.filter((item) => Number(item) !== Number(id))
    );
  }

  function formatScore(value) {
    return value !== null &&
      value !== undefined &&
      value !== "" &&
      Number.isFinite(Number(value))
      ? `${Number(value).toFixed(1)}/100`
      : "Not rated";
  }

  function formatPrice(product) {
    if (product.price === null || product.price === undefined)
      return "Price unavailable";
    try {
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: product.currency || "INR",
        maximumFractionDigits: 0,
      }).format(Number(product.price));
    } catch {
      return `₹${product.price}`;
    }
  }

  function bestIndex(field) {
    const values = compared.map((p) => {
      const v = p[field];
      return v !== null && v !== undefined && Number.isFinite(Number(v)) ? Number(v) : -Infinity;
    });
    const max = Math.max(...values);
    return max === -Infinity ? -1 : values.indexOf(max);
  }

  function ScoreBar({ value }) {
    const num = Number(value);
    const valid = value !== null && value !== undefined && Number.isFinite(num);
    return (
      <div className="score-track" style={{ marginTop: 6, minWidth: 80 }}>
        <div
          className="score-fill"
          style={{ width: valid ? `${Math.max(0, Math.min(100, num))}%` : "0%" }}
        />
      </div>
    );
  }

  return (
    <main className="comparison-page">
      {/* Page intro */}
      <section className="page-intro" aria-labelledby="compare-heading">
        <div style={{ maxWidth: "var(--max-w-content)", margin: "0 auto" }}>
          <span className="eyebrow">Evidence-Based Consumer Analysis</span>
          <h1 id="compare-heading">
            Compare Brands: <em>Health & Eco Impact</em>
          </h1>
          <p>
            Evaluate similar products across different brands to discover which option is
            healthier for you and gentler on the planet.
          </p>

          {/* Mode Switcher Tabs */}
          <div className="compare-mode-tabs" role="tablist">
            <button
              role="tab"
              aria-selected={activeTab === "online"}
              className={`compare-tab-btn ${activeTab === "online" ? "active" : ""}`}
              onClick={() => setActiveTab("online")}
            >
              🌐 Live Online Brand Comparison (Open Food Facts)
            </button>
            <button
              role="tab"
              aria-selected={activeTab === "catalog"}
              className={`compare-tab-btn ${activeTab === "catalog" ? "active" : ""}`}
              onClick={() => setActiveTab("catalog")}
            >
              📦 GreenCart Catalog ({compared.length} selected)
            </button>
          </div>
        </div>
      </section>

      {/* Main content based on active tab */}
      <div className="section-wrap">
        {activeTab === "online" ? (
          <OnlineBrandCompare />
        ) : (
          <>
            {/* Catalog header row */}
            <div className="section-header">
              <div className="section-header-text">
                <h2>GreenCart Catalog Comparison</h2>
                <p>{compared.length} of 3 products selected</p>
              </div>
              <Link className="secondary-button" to="/products">
                + Add products from shop
              </Link>
            </div>

            {loading ? (
              <div className="comparison-empty" role="status">
                <div className="comparison-empty-icon" aria-hidden="true">⏳</div>
                <h3>Loading your comparison…</h3>
                <p>Fetching product data from the GreenCart backend.</p>
              </div>
            ) : error ? (
              <div className="comparison-empty" role="alert">
                <div className="comparison-empty-icon" aria-hidden="true">⚠️</div>
                <h3>Unable to load products</h3>
                <p>{error}</p>
                <button className="primary-button" onClick={() => window.location.reload()}>
                  Try again
                </button>
              </div>
            ) : compared.length === 0 ? (
              <div className="comparison-empty" role="status">
                <div className="comparison-empty-icon" aria-hidden="true">⚖️</div>
                <h3>No catalog products selected yet</h3>
                <p>
                  Browse our catalog and click <strong>&ldquo;+ Compare&rdquo;</strong> on any product card, or switch to the{" "}
                  <strong style={{ cursor: "pointer", color: "var(--clr-primary)" }} onClick={() => setActiveTab("online")}>
                    Live Online Brand Comparison
                  </strong>{" "}
                  tab to search any brand online.
                </p>
                <div style={{ display: "flex", gap: "12px", justifyContent: "center", marginTop: "16px" }}>
                  <button className="primary-button" onClick={() => setActiveTab("online")}>
                    Try Live Brand Comparison →
                  </button>
                  <Link className="secondary-button" to="/products">
                    Browse Catalog
                  </Link>
                </div>
              </div>
            ) : (
              <div className="comparison-table-wrap">
                <table className="comparison-table">
                  <thead>
                    <tr>
                      <th scope="col">Product details</th>
                      {compared.map((product) => (
                        <th scope="col" key={product.id}>
                          <div className="comparison-col-header">
                            {product.image_url ? (
                              <img
                                src={product.image_url}
                                alt={product.name}
                                className="comparison-product-image"
                              />
                            ) : (
                              <div className="comparison-product-icon" aria-hidden="true">♻️</div>
                            )}
                            <span>{product.name}</span>
                            <small>{product.brand || "Brand unavailable"}</small>
                          </div>
                        </th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>
                    <tr>
                      <th scope="row">Category</th>
                      {compared.map((p) => (
                        <td key={p.id}>{p.category?.name || "—"}</td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Product Type</th>
                      {compared.map((p) => (
                        <td key={p.id}>
                          <span className={`badge-pill ${p.is_sustainable ? "sustainable" : "conventional"}`}>
                            {p.is_sustainable ? "🌱 Sustainable Alternative" : "Conventional Product"}
                          </span>
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Price</th>
                      {compared.map((p, i) => {
                        const best =
                          bestIndex("price") === -1
                            ? -1
                            : compared.reduce(
                                (minIdx, prod, idx) =>
                                  Number(prod.price) < Number(compared[minIdx].price) ? idx : minIdx,
                                0
                              );
                        return (
                          <td key={p.id} className={i === best ? "best-score" : ""}>
                            <strong>{formatPrice(p)}</strong>
                          </td>
                        );
                      })}
                    </tr>

                    <tr>
                      <th scope="row">Materials & Composition</th>
                      {compared.map((p) => (
                        <td key={p.id} style={{ fontSize: 13, lineHeight: 1.5 }}>
                          {p.materials || "Standard conventional materials"}
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Durability</th>
                      {compared.map((p, i) => (
                        <td key={p.id} className={i === bestIndex("durability_score") ? "best-score" : ""}>
                          <span className={i === bestIndex("durability_score") ? "score-value" : ""}>
                            {formatScore(p.durability_score)}
                          </span>
                          <ScoreBar value={p.durability_score} />
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Packaging Eco-Rating</th>
                      {compared.map((p, i) => (
                        <td key={p.id} className={i === bestIndex("packaging_score") ? "best-score" : ""}>
                          <span className={i === bestIndex("packaging_score") ? "score-value" : ""}>
                            {formatScore(p.packaging_score)}
                          </span>
                          <ScoreBar value={p.packaging_score} />
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Overall Sustainability Score</th>
                      {compared.map((p, i) => (
                        <td key={p.id} className={i === bestIndex("overall_sustainability_score") ? "best-score" : ""}>
                          <strong className={i === bestIndex("overall_sustainability_score") ? "score-value" : ""}>
                            {formatScore(p.overall_sustainability_score)}
                          </strong>
                          <ScoreBar value={p.overall_sustainability_score} />
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <th scope="row">Action</th>
                      {compared.map((p) => (
                        <td key={p.id}>
                          <button
                            className="remove-button"
                            onClick={() => removeProduct(p.id)}
                            aria-label={`Remove ${p.name} from comparison`}
                          >
                            ✕ Remove
                          </button>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
}

export default Compare;
