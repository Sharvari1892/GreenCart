import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api";

function Compare({ selectedProducts = [], setSelectedProducts }) {
  const [products, setProducts] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState("");

  useEffect(() => {
    let cancelled = false;

    async function fetchProducts() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_URL}/products?page=1&page_size=100`);
        if (!response.ok) throw new Error("Could not load products from the server.");

        const data = await response.json();
        const items = Array.isArray(data) ? data : (data.items || []);
        if (!cancelled) setProducts(items);
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load products.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchProducts();
    return () => { cancelled = true; };
  }, []);

  /* Products currently being compared */
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
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: product.currency || "USD",
      }).format(Number(product.price));
    } catch {
      return `${product.price} ${product.currency || "USD"}`;
    }
  }

  /**
   * Returns the index of the product with the highest numeric value
   * for a given field (for "best" highlight). Returns -1 if all are unrated.
   */
  function bestIndex(field) {
    const values = compared.map((p) => {
      const v = p[field];
      return v !== null && v !== undefined && Number.isFinite(Number(v)) ? Number(v) : -Infinity;
    });
    const max = Math.max(...values);
    return max === -Infinity ? -1 : values.indexOf(max);
  }

  /* Score bar helper */
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

  /* ── Render ─────────────────────────────────────────────── */
  return (
    <main className="comparison-page">
      {/* Page intro */}
      <section className="page-intro" aria-labelledby="compare-heading">
        <div style={{ maxWidth: "var(--max-w-content)", margin: "0 auto" }}>
          <span className="eyebrow">Make an informed decision</span>
          <h1 id="compare-heading">
            Compare your <em>choices.</em>
          </h1>
          <p>
            Review product prices and sustainability information side by side
            — up to 3 products at once.
          </p>
        </div>
      </section>

      {/* Main content */}
      <div className="section-wrap">
        {/* Header row */}
        <div className="section-header">
          <div className="section-header-text">
            <h2>Your comparison</h2>
            <p>{compared.length} of 3 products selected</p>
          </div>
          <Link className="secondary-button" to="/products">
            + Add products
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
            <h3>Let&rsquo;s compare some products</h3>
            <p>
              Head to the Products page and tap <strong>&ldquo;+ Compare&rdquo;</strong>{" "}
              on up to 3 products. They&rsquo;ll appear here automatically.
            </p>
            <Link className="primary-button" to="/products">
              Browse products →
            </Link>
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
                {/* Category */}
                <tr>
                  <th scope="row">Category</th>
                  {compared.map((p) => (
                    <td key={p.id}>{p.category?.name || "—"}</td>
                  ))}
                </tr>

                {/* Price */}
                <tr>
                  <th scope="row">Price</th>
                  {compared.map((p, i) => {
                    const best = bestIndex("price") === -1
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

                {/* Durability */}
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

                {/* Packaging */}
                <tr>
                  <th scope="row">Packaging</th>
                  {compared.map((p, i) => (
                    <td key={p.id} className={i === bestIndex("packaging_score") ? "best-score" : ""}>
                      <span className={i === bestIndex("packaging_score") ? "score-value" : ""}>
                        {formatScore(p.packaging_score)}
                      </span>
                      <ScoreBar value={p.packaging_score} />
                    </td>
                  ))}
                </tr>

                {/* Repairability */}
                <tr>
                  <th scope="row">Repairability</th>
                  {compared.map((p, i) => (
                    <td key={p.id} className={i === bestIndex("repairability_score") ? "best-score" : ""}>
                      <span className={i === bestIndex("repairability_score") ? "score-value" : ""}>
                        {formatScore(p.repairability_score)}
                      </span>
                      <ScoreBar value={p.repairability_score} />
                    </td>
                  ))}
                </tr>

                {/* Overall sustainability */}
                <tr>
                  <th scope="row">Overall sustainability</th>
                  {compared.map((p, i) => (
                    <td key={p.id} className={i === bestIndex("overall_sustainability_score") ? "best-score" : ""}>
                      <span className="score-value">
                        {formatScore(p.overall_sustainability_score)}
                      </span>
                      <ScoreBar value={p.overall_sustainability_score} />
                    </td>
                  ))}
                </tr>

                {/* Evidence coverage */}
                <tr>
                  <th scope="row">Evidence coverage</th>
                  {compared.map((p, i) => (
                    <td key={p.id} className={i === bestIndex("evidence_coverage") ? "best-score" : ""}>
                      <span className={i === bestIndex("evidence_coverage") ? "score-value" : ""}>
                        {formatScore(p.evidence_coverage)}
                      </span>
                      <ScoreBar value={p.evidence_coverage} />
                    </td>
                  ))}
                </tr>

                {/* Description */}
                <tr>
                  <th scope="row">Description</th>
                  {compared.map((p) => (
                    <td key={p.id} style={{ fontSize: 12, lineHeight: 1.6, color: "var(--clr-text-muted)" }}>
                      {p.description || "No description available"}
                    </td>
                  ))}
                </tr>

                {/* Remove action */}
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

        <p className="demo-note">
          Scores reflect currently available product data and verified evidence.
          Missing scores are shown as "Not rated". 🟢 Green highlight = best value in that row.
        </p>
      </div>
    </main>
  );
}

export default Compare;
