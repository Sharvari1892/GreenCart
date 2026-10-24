
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000/api";

function Products({ selectedProducts, setSelectedProducts }) {
  console.log("Selected product IDs:", selectedProducts);
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [categoryList, setCategoryList] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const controller = new AbortController();

    async function fetchProducts() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `${API_URL}/products?page=1&page_size=100`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error(`Failed to load products (${response.status}).`);
        }

        const data = await response.json();
        setProducts(data.items || []);
        const categoryResponse = await fetch(`${API_URL}/categories`, {
  signal: controller.signal,
});

if (categoryResponse.ok) {
  const categoryData = await categoryResponse.json();
  setCategoryList(categoryData);
}
      } catch (err) {
        if (err.name !== "AbortError") {
          setError(err.message || "Unable to load products.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    fetchProducts();

    return () => controller.abort();
  }, []);

  const categoryNames = useMemo(
  () => new Map(categoryList.map((item) => [item.id, item.name])),
  [categoryList]
);

  
const getCategoryName = (product) =>
  categoryNames.get(product.category_id) ||
  product.category ||
  `Category ${product.category_id}`;


const categories = useMemo(
  () => ["All", ...new Set(products.map(getCategoryName))],
  [products, categoryNames]
);

  const filteredProducts = products.filter((product) => {
    const query = search.toLowerCase();

    const matchesSearch = [
      product.name,
      product.brand,
      product.description,
    ].some((value) => (value || "").toLowerCase().includes(query));

    const productCategory =
      getCategoryName(product)

    const matchesCategory =
      category === "All" || productCategory === category;

    return matchesSearch && matchesCategory;
  });

  
function toggleCompare(id) {
  setSelectedProducts((current) => {
    if (current.includes(id)) {
      return current.filter((item) => item !== id);
    }

    if (current.length >= 3) {
      return current;
    }

    const updated = [...current, id];

    if (updated.length === 3) {
      setTimeout(() => {
        navigate("/compare");
      }, 0);
    }

    return updated;
  });
}


  function formatPrice(product) {
    const currency = product.currency || "USD";

    try {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency,
        maximumFractionDigits: 2,
      }).format(Number(product.price));
    } catch {
      return `${product.price} ${currency}`;
    }
  }

  return (
    <main className="products-page">
      <section className="products-intro">
        <span className="eyebrow">THOUGHTFUL SHOPPING STARTS HERE</span>
        <h1>
          Discover <span>better choices.</span>
        </h1>
        <p>
          Explore everyday essentials and compare their sustainability
          information before you choose.
        </p>
      </section>

      <section className="products-section">
        <div className="section-heading">
          <div>
            <h2>Explore products</h2>
            <p>Find products that fit your needs.</p>
          </div>
          <span className="product-count">
            {loading ? "Loading..." : `${filteredProducts.length} products`}
          </span>
        </div>

        <div className="filters">
          <label className="search-box">
            <span>⌕</span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search products..."
              aria-label="Search products"
            />
          </label>

          <label className="category-filter">
            <span className="sr-only">Filter by category</span>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              {categories.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
        </div>

        {loading ? (
          <div className="no-results">
            <h3>Loading products...</h3>
            <p>Fetching the latest products from GreenCart.</p>
          </div>
        ) : error ? (
          <div className="no-results">
            <h3>Couldn't load products</h3>
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>
              Try again
            </button>
          </div>
        ) : filteredProducts.length > 0 ? (
          <div className="product-grid">
            {filteredProducts.map((product) => {
              const isSelected = selectedProducts.includes(product.id);
              const score = product.overall_sustainability_score;
              const hasScore =
                score !== null &&
                score !== undefined &&
                score !== "" &&
                Number.isFinite(Number(score));
              const productCategory = getCategoryName(product);

              return (
                <article className="product-card" key={product.id}>
                  <div className={`product-visual visual-${product.id}`}>
                    <span className="eco-tag">♻ Sustainability</span>

                    {product.image_url ? (
                      <img
                        className="product-emoji"
                        src={product.image_url}
                        alt={product.name}
                        style={{
                          width: "100%",
                          height: "100%",
                          objectFit: "contain",
                        }}
                      />
                    ) : (
                      <span className="product-emoji" aria-hidden="true">
                        ♻️
                      </span>
                    )}

                    <button
                      className={`compare-toggle ${
                        isSelected ? "chosen" : ""
                      }`}
                      onClick={() => toggleCompare(product.id)}
                      aria-label={`${
                        isSelected ? "Remove" : "Add"
                      } ${product.name} ${
                        isSelected ? "from" : "to"
                      } comparison`}
                      aria-pressed={isSelected}
                    >
                      {isSelected ? "✓" : "+"}
                    </button>
                  </div>

                  <div className="product-info">
                    <span className="product-category">
                      {productCategory}
                    </span>

                    <h3>{product.name}</h3>

                    {product.brand && (
                      <p className="product-brand">{product.brand}</p>
                    )}

                    <p>
                      {product.description || "Product details unavailable."}
                    </p>

                    <div className="eco-score">
                      <div>
                        <span>Sustainability score</span>
                        <strong>
                          {hasScore ? `${Number(score).toFixed(1)}/100` : "Not rated"}
                        </strong>
                      </div>

                      <div className="score-track">
                        <div
                          style={{
                            width: `${
                              hasScore
                                ? Math.min(100, Math.max(0, score))
                                : 0
                            }%`,
                          }}
                        />
                      </div>
                    </div>

                    <div className="product-footer">
                      <div>
                        <strong>{formatPrice(product)}</strong>
                      </div>

                      <button
                        className="compare-button"
                        onClick={() => toggleCompare(product.id)}
                      >
                        {isSelected ? "Selected ✓" : "Compare +"}
                      </button>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="no-results">
            <span>🔎</span>
            <h3>
              {products.length === 0
                ? "No products available"
                : "No matching products"}
            </h3>
            <p>
              {products.length === 0
                ? "Add products to your database to display them here."
                : "Try another search term or choose a different category."}
            </p>

            {products.length > 0 && (
              <button
                onClick={() => {
                  setSearch("");
                  setCategory("All");
                }}
              >
                Clear filters
              </button>
            )}
          </div>
        )}

        <p className="demo-note">
          Product information and sustainability scores are provided by the
          GreenCart backend.
        </p>
      </section>
    </main>
  );
}

export default Products;
