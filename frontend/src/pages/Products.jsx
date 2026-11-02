import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import LoadingSkeleton from "../components/LoadingSkeleton";

const API_URL = "http://127.0.0.1:8000/api";

const SORT_OPTIONS = [
  { value: "",                     label: "Default order" },
  { value: "name|asc",             label: "Name A→Z" },
  { value: "name|desc",            label: "Name Z→A" },
  { value: "price|asc",            label: "Price: Low to High" },
  { value: "price|desc",           label: "Price: High to Low" },
  { value: "sustainability_score|desc", label: "Best Sustainability" },
];

function Products({ selectedProducts, setSelectedProducts }) {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  /* ── State ──────────────────────────────────────────────── */
  const [products,     setProducts]     = useState([]);
  const [search,       setSearch]       = useState("");
  const [category,     setCategory]     = useState("All");
  const [sort,         setSort]         = useState("");
  const [loading,      setLoading]      = useState(true);
  const [error,        setError]        = useState("");
  const [categoryList, setCategoryList] = useState([]);
  const [catFromUrl,   setCatFromUrl]   = useState(false);

  /* ── Fetch products + categories on mount ───────────────── */
  useEffect(() => {
    const controller = new AbortController();

    async function fetchAll() {
      try {
        setLoading(true);
        setError("");

        const [prodRes, catRes] = await Promise.all([
          fetch(`${API_URL}/products?page=1&page_size=100`, { signal: controller.signal }),
          fetch(`${API_URL}/categories`, { signal: controller.signal }),
        ]);

        if (!prodRes.ok) {
          throw new Error(`Failed to load products (${prodRes.status}).`);
        }

        const prodData = await prodRes.json();
        setProducts(prodData.items || []);

        if (catRes.ok) {
          const catData = await catRes.json();
          setCategoryList(Array.isArray(catData) ? catData : []);
        }
      } catch (err) {
        if (err.name !== "AbortError") {
          setError(err.message || "Unable to load products.");
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    fetchAll();
    return () => controller.abort();
  }, []);

  /* Honour ?category=<id> from query string (e.g. from Home page category click).
     We do this in render (not in an effect) to avoid cascading renders. */
  const catIdParam = searchParams.get("category");

  /* ── Derived data ───────────────────────────────────────── */
  const categoryNames = useMemo(
    () => new Map(categoryList.map((item) => [item.id, item.name])),
    [categoryList]
  );

  /* Stable helper — defined outside useMemo so we can use it inline */
  const getCategoryName = (product) =>
    categoryNames.get(product.category_id) ||
    product.category?.name ||
    `Category ${product.category_id}`;

  /* Resolve URL category param to a name once categories are loaded */
  const resolvedCatFromUrl = useMemo(() => {
    if (!catIdParam || categoryList.length === 0) return null;
    const found = categoryList.find((c) => String(c.id) === String(catIdParam));
    return found ? found.name : null;
  }, [catIdParam, categoryList]);

  /* Effective category — URL param takes precedence until user selects a pill */
  const effectiveCategory = !catFromUrl && resolvedCatFromUrl ? resolvedCatFromUrl : category;

  /* All distinct categories from loaded products */
  const allCategories = useMemo(
    () => ["All", ...new Set(products.map((p) => getCategoryName(p)))],
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [products, categoryNames]
  );

  /* Filter by search + category */
  const filteredProducts = useMemo(() => {
    const query = search.toLowerCase().trim();
    let result = products.filter((product) => {
      const matchesSearch = !query || [product.name, product.brand, product.description, product.materials]
        .some((v) => (v || "").toLowerCase().includes(query));
      const productCategory =
        categoryNames.get(product.category_id) || product.category?.name || `Category ${product.category_id}`;
      const matchesCategory = effectiveCategory === "All" || productCategory === effectiveCategory;
      return matchesSearch && matchesCategory;
    });

    /* Client-side sort (supplements backend default ordering) */
    if (sort) {
      const [field, dir] = sort.split("|");
      result = [...result].sort((a, b) => {
        let aVal = a[field === "sustainability_score" ? "overall_sustainability_score" : field] ?? 0;
        let bVal = b[field === "sustainability_score" ? "overall_sustainability_score" : field] ?? 0;
        if (typeof aVal === "string") aVal = aVal.toLowerCase();
        if (typeof bVal === "string") bVal = bVal.toLowerCase();
        if (aVal < bVal) return dir === "asc" ? -1 : 1;
        if (aVal > bVal) return dir === "asc" ? 1 : -1;
        return 0;
      });
    }

    return result;
  }, [products, search, effectiveCategory, sort, categoryNames]);

  /* ── Compare toggle ─────────────────────────────────────── */
  function toggleCompare(id) {
    setSelectedProducts((current) => {
      if (current.includes(id)) return current.filter((item) => item !== id);
      if (current.length >= 3) return current;
      const updated = [...current, id];
      if (updated.length === 3) {
        setTimeout(() => navigate("/compare"), 0);
      }
      return updated;
    });
  }

  /* ── Render ─────────────────────────────────────────────── */
  return (
    <main className="products-page">
      {/* Page intro header */}
      <section className="page-intro" aria-labelledby="products-heading">
        <div style={{ maxWidth: "var(--max-w-content)", margin: "0 auto" }}>
          <span className="eyebrow">Thoughtful shopping starts here</span>
          <h1 id="products-heading">
            Discover <em>better choices.</em>
          </h1>
          <p>
            Explore everyday essentials and compare their sustainability
            information before you choose.
          </p>
        </div>
      </section>

      {/* Main content */}
      <div className="section-wrap">
        {/* Search + sort toolbar */}
        <div className="products-toolbar" role="search">
          <label className="search-box" style={{ flex: "1 1 260px" }}>
            <span className="search-icon" aria-hidden="true">⌕</span>
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search products by name, brand or description…"
              aria-label="Search products"
            />
          </label>

          <label className="sr-only" htmlFor="sort-select">Sort products</label>
          <select
            id="sort-select"
            className="sort-select"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            aria-label="Sort products"
          >
            {SORT_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>

        {/* Category pills */}
        {!loading && categoryList.length > 0 && (
          <div className="category-pills" role="group" aria-label="Filter by category">
            {allCategories.map((cat) => (
              <button
                key={cat}
                className={`category-pill${effectiveCategory === cat ? " active" : ""}`}
                onClick={() => { setCategory(cat); setCatFromUrl(true); }}
                aria-pressed={effectiveCategory === cat}
              >
                {cat}
              </button>
            ))}
          </div>
        )}

        {/* Header row with count + clear */}
        <div className="products-header-row">
          <h2>Explore products</h2>
          <div style={{ display: "flex", gap: "var(--space-3)", alignItems: "center", flexWrap: "wrap" }}>
            {(search || effectiveCategory !== "All") && (
              <button
                className="secondary-button"
                style={{ padding: "8px 14px", fontSize: 13 }}
                onClick={() => { setSearch(""); setCategory("All"); setCatFromUrl(true); }}
              >
                ✕ Clear filters
              </button>
            )}
            <span className="product-count-badge">
              {loading ? "Loading…" : `${filteredProducts.length} product${filteredProducts.length !== 1 ? "s" : ""}`}
            </span>
          </div>
        </div>

        {/* Product grid / states */}
        {loading ? (
          <LoadingSkeleton count={6} />
        ) : error ? (
          <div className="no-results" role="alert">
            <div className="no-results-icon">⚠️</div>
            <h3>Couldn&rsquo;t load products</h3>
            <p>{error}</p>
            <button className="primary-button" onClick={() => window.location.reload()}>
              Try again
            </button>
          </div>
        ) : filteredProducts.length > 0 ? (
          <div className="product-grid">
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                categoryName={getCategoryName(product)}
                isSelected={selectedProducts.includes(product.id)}
                onToggleCompare={toggleCompare}
              />
            ))}
          </div>
        ) : (
          <div className="no-results" role="status">
            <div className="no-results-icon">🔎</div>
            <h3>
              {products.length === 0 ? "No products available" : "No matching products"}
            </h3>
            <p>
              {products.length === 0
                ? "Add products to your database to display them here."
                : "Try another search term or choose a different category."}
            </p>
            {products.length > 0 && (
              <button
                className="primary-button"
                onClick={() => { setSearch(""); setCategory("All"); }}
              >
                Clear filters
              </button>
            )}
          </div>
        )}

        <p className="demo-note">
          Product information and sustainability scores are provided by the GreenCart backend.
        </p>
      </div>
    </main>
  );
}

export default Products;
