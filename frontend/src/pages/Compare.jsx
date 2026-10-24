
import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

const API_URL = "http://127.0.0.1:8000/api";

function Compare({ selectedProducts = [], setSelectedProducts }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function fetchProducts() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_URL}/products`);

        if (!response.ok) {
          throw new Error("Could not load products from the server.");
        }

        const data = await response.json();
        const items = Array.isArray(data) ? data : data.items || [];

        if (!cancelled) {
          setProducts(items);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Failed to load products.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchProducts();

    return () => {
      cancelled = true;
    };
  }, []);

  const compared = useMemo(() => {
    const ids = selectedProducts.map(Number);
    return products.filter((product) => ids.includes(Number(product.id)));
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
    if (product.price === null || product.price === undefined) {
      return "Price unavailable";
    }

    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: product.currency || "USD",
    }).format(Number(product.price));
  }

  return (
    <main className="comparison-page">
      <section className="products-intro">
        <span className="eyebrow">MAKE AN INFORMED DECISION</span>
        <h1>
          Compare your <span>choices.</span>
        </h1>
        <p>
          Review product prices and sustainability information side by side.
        </p>
      </section>

      <section className="comparison-section">
        <div className="section-heading">
          <div>
            <h2>Your comparison</h2>
            <p>{compared.length} of 3 products selected</p>
          </div>
          <Link className="secondary-button" to="/products">
            + Add products
          </Link>
        </div>

        {loading ? (
          <div className="comparison-empty">
            <h3>Loading your comparison...</h3>
          </div>
        ) : error ? (
          <div className="comparison-empty">
            <h3>Unable to load products</h3>
            <p>{error}</p>
            <button
              className="primary-button"
              onClick={() => window.location.reload()}
            >
              Try again
            </button>
          </div>
        ) : compared.length === 0 ? (
          <div className="comparison-empty">
            <span>⚖️</span>
            <h3>Let's compare some products</h3>
            <p>
              Select products on the Products page to compare their actual
              sustainability information.
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
                      {product.image_url ? (
                        <img
                          src={product.image_url}
                          alt={product.name}
                          className="comparison-product-image"
                        />
                      ) : (
                        <span className="comparison-product-icon">♻️</span>
                      )}
                      <span>{product.name}</span>
                      <small>{product.brand || "Brand unavailable"}</small>
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
                  <th scope="row">Price</th>
                  {compared.map((p) => (
                    <td key={p.id}>
                      <strong>{formatPrice(p)}</strong>
                    </td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Durability</th>
                  {compared.map((p) => (
                    <td key={p.id}>{formatScore(p.durability_score)}</td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Packaging</th>
                  {compared.map((p) => (
                    <td key={p.id}>{formatScore(p.packaging_score)}</td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Repairability</th>
                  {compared.map((p) => (
                    <td key={p.id}>{formatScore(p.repairability_score)}</td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Overall sustainability</th>
                  {compared.map((p) => (
                    <td key={p.id}>
                      <strong className="score-value">
                        {formatScore(p.overall_sustainability_score)}
                      </strong>
                      {p.overall_sustainability_score != null && (
                        <div className="score-track">
                          <div
                            style={{
                              width: `${Math.max(
                                0,
                                Math.min(
                                  100,
                                  Number(p.overall_sustainability_score)
                                )
                              )}%`,
                            }}
                          />
                        </div>
                      )}
                    </td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Verified evidence coverage</th>
                  {compared.map((p) => (
                    <td key={p.id}>
                      {formatScore(p.evidence_coverage)}
                    </td>
                  ))}
                </tr>

                <tr>
                  <th scope="row">Description</th>
                  {compared.map((p) => (
                    <td key={p.id}>
                      {p.description || "No description available"}
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
                      >
                        Remove
                      </button>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        )}

        <p className="demo-note">
          Scores reflect the currently available product data and verified
          evidence. Missing scores are shown as not rated.
        </p>
      </section>
    </main>
  );
}

export default Compare;
