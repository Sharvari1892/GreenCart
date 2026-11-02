import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { Link } from "react-router-dom";
import LoadingSkeleton from "../components/LoadingSkeleton";

const API_URL = "http://127.0.0.1:8000/api";

/** Format price in INR */
function formatPrice(price, currency = "INR") {
  if (price === null || price === undefined || price === "") {
    return "Price unavailable";
  }
  try {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: currency || "INR",
      maximumFractionDigits: 0,
    }).format(Number(price));
  } catch {
    return `₹${price}`;
  }
}

/** Human-readable replacement type label */
function formatReplacementType(type) {
  if (!type) return "Type not specified";
  switch (type.toLowerCase()) {
    case "composition_change":
      return "Composition change";
    case "design_change":
      return "Design change";
    case "entire_product_replacement":
      return "Entire-product replacement";
    default:
      return type.replace(/_/g, " ");
  }
}

/** Get class name for replacement type */
function getReplacementTypeClass(type) {
  if (!type) return "type-generic";
  switch (type.toLowerCase()) {
    case "composition_change":
      return "type-composition";
    case "design_change":
      return "type-design";
    case "entire_product_replacement":
      return "type-entire";
    default:
      return "type-generic";
  }
}

/** Source verification metadata helper */
function getSourceMeta(status, purchaseUrl) {
  if (!purchaseUrl) return null;
  switch (status) {
    case "verified_exact_source":
      return {
        label: "Verified Store ↗",
        badge: "Direct Store",
        className: "source-badge-verified",
        title: "Direct purchase page from verified merchant/brand store",
      };
    case "manufacturer_info_only":
      return {
        label: "Manufacturer Info ↗",
        badge: "Manufacturer Spec",
        className: "source-badge-mfg",
        title: "Official manufacturer specification / catalogue page",
      };
    case "retailer_source":
      return {
        label: "Retailer Listing ↗",
        badge: "Retailer",
        className: "source-badge-retailer",
        title: "Third-party retailer / marketplace listing",
      };
    default:
      return {
        label: "Reference Source ↗",
        badge: "Reference",
        className: "source-badge-unverified",
        title: "Regulatory reference or unverified source",
      };
  }
}

/** Evidence badge helper */
function getEvidenceBadge(product) {
  const coverage = Number(product.evidence_coverage) || 0;
  if (coverage >= 60) {
    return {
      className: "verified",
      label: `✓ Certified Evidence (${Math.round(coverage)}%)`,
      title: `${Math.round(coverage)}% independently verified sustainability evidence`,
    };
  }
  if (coverage > 0) {
    return {
      className: "verified",
      label: `✓ Partial Evidence (${Math.round(coverage)}%)`,
      title: `${Math.round(coverage)}% verified evidence coverage`,
    };
  }
  if (product.source_verification_status === "manufacturer_info_only" || product.materials) {
    return {
      className: "manufacturer",
      label: "ℹ️ Manufacturer-Reported",
      title: "Material specifications are self-reported by manufacturer without third-party audit",
    };
  }
  return {
    className: "unverified",
    label: "— Unverified / No Evidence",
    title: "No verified evidence or environmental certifications available",
  };
}

/** Helper to detect shared composition or function */
function getSharedProperties(orig, rep) {
  if (!orig || !rep) return null;
  const shared = [];
  const origMat = (orig.materials || "").toLowerCase();
  const repMat = (rep.materials || "").toLowerCase();

  if (origMat && repMat) {
    const commonTerms = ["nylon", "cotton", "steel", "glass", "paper", "wood", "bristles", "canvas", "corrugated"];
    for (const term of commonTerms) {
      if (origMat.includes(term) && repMat.includes(term)) {
        shared.push(`Both products utilize ${term} components.`);
      }
    }
  }

  if (shared.length === 0) {
    if (orig.category_id && orig.category_id === rep.category_id) {
      shared.push("Both products fulfill the same functional category role without requiring lifestyle workflow changes.");
    }
  }

  return shared.length > 0 ? shared : null;
}

function Replacements({ selectedProducts = [], setSelectedProducts }) {
  const explanationRef = useRef(null);

  /* ── State ──────────────────────────────────────────────── */
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [errorProducts, setErrorProducts] = useState("");

  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const [selectedProduct, setSelectedProduct] = useState(null);
  const [replacements, setReplacements] = useState([]);
  const [loadingReplacements, setLoadingReplacements] = useState(false);
  const [errorReplacements, setErrorReplacements] = useState("");

  const [activeReplacement, setActiveReplacement] = useState(null);
  const [toast, setToast] = useState(null);

  /* ── Debounce search ────────────────────────────────────── */
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
    }, 250);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  /* ── Toast auto-dismiss ─────────────────────────────────── */
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 4500);
    return () => clearTimeout(timer);
  }, [toast]);

  /* ── Fetch products and categories on mount ─────────────── */
  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoadingProducts(true);
        setErrorProducts("");

        const [prodRes, catRes] = await Promise.all([
          fetch(`${API_URL}/products?page=1&page_size=100`),
          fetch(`${API_URL}/categories`),
        ]);

        if (!prodRes.ok) throw new Error("Could not load products catalogue.");
        const prodData = await prodRes.json();
        const catData = catRes.ok ? await catRes.json() : [];

        if (!cancelled) {
          setProducts(prodData.items || []);
          setCategories(Array.isArray(catData) ? catData : []);
        }
      } catch (err) {
        if (!cancelled) setErrorProducts(err.message || "Failed to load products.");
      } finally {
        if (!cancelled) setLoadingProducts(false);
      }
    }

    loadData();
    return () => {
      cancelled = true;
    };
  }, []);

  /* ── Category mapping ───────────────────────────────────── */
  const categoryMap = useMemo(() => {
    return new Map(categories.map((c) => [c.id, c.name]));
  }, [categories]);

  const getCategoryName = useCallback(
    (product) => {
      if (!product) return "General";
      return categoryMap.get(product.category_id) || product.category?.name || "General";
    },
    [categoryMap]
  );

  /* ── Fetch replacements when selectedProduct changes ────── */
  useEffect(() => {
    if (!selectedProduct) return;

    let cancelled = false;

    async function loadReplacements() {
      try {
        setLoadingReplacements(true);
        setErrorReplacements("");

        const res = await fetch(`${API_URL}/products/${selectedProduct.id}/replacements`);
        if (!res.ok) {
          if (res.status === 404) {
            throw new Error("Product not found.");
          }
          throw new Error("Unable to load replacement alternatives.");
        }

        const data = await res.json();
        if (!cancelled) {
          const list = Array.isArray(data) ? data : [];
          setReplacements(list);
          if (list.length > 0) {
            setActiveReplacement(list[0]);
          } else {
            setActiveReplacement(null);
          }
        }
      } catch (err) {
        if (!cancelled) setErrorReplacements(err.message || "Error loading replacements.");
      } finally {
        if (!cancelled) setLoadingReplacements(false);
      }
    }

    loadReplacements();
    return () => {
      cancelled = true;
    };
  }, [selectedProduct]);

  /* ── Conventional products list for Section C ───────────── */
  const conventionalProducts = useMemo(() => {
    const q = debouncedSearch.toLowerCase().trim();
    return products.filter((p) => {
      const isConventional = !p.is_sustainable;
      if (!isConventional) return false;

      // Category filter
      if (selectedCategory !== "All") {
        const catName = getCategoryName(p);
        if (catName !== selectedCategory) return false;
      }

      // Search filter across name, brand, materials, description, category
      if (q) {
        const catName = getCategoryName(p).toLowerCase();
        const match =
          (p.name || "").toLowerCase().includes(q) ||
          (p.brand || "").toLowerCase().includes(q) ||
          (p.materials || "").toLowerCase().includes(q) ||
          (p.description || "").toLowerCase().includes(q) ||
          catName.includes(q);
        if (!match) return false;
      }

      return true;
    });
  }, [products, debouncedSearch, selectedCategory, getCategoryName]);

  /* ── Handlers ───────────────────────────────────────────── */
  const handleSelectProduct = (product) => {
    if (selectedProduct && selectedProduct.id === product.id) {
      // Deselect
      setSelectedProduct(null);
      setReplacements([]);
      setActiveReplacement(null);
    } else {
      setSelectedProduct(product);
    }
  };

  const handleClearSelection = () => {
    setSelectedProduct(null);
    setReplacements([]);
    setActiveReplacement(null);
  };

  const handleCompare = (replacementItem) => {
    if (!selectedProduct || !replacementItem) return;
    const repProd = replacementItem.replacement_product;

    setSelectedProducts((current) => {
      const idsToAdd = [selectedProduct.id, repProd.id];
      const merged = [...current];
      for (const id of idsToAdd) {
        if (!merged.includes(id)) {
          if (merged.length < 3) {
            merged.push(id);
          }
        }
      }
      return merged;
    });

    setToast({
      message: `Added "${selectedProduct.name}" and "${repProd.name}" to comparison.`,
      actionText: "Open comparison →",
      actionLink: "/compare",
    });
  };

  const handleViewExplanation = (rep) => {
    setActiveReplacement(rep);
    if (explanationRef.current) {
      explanationRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  /* ── Render ─────────────────────────────────────────────── */
  return (
    <main className="replacements-page">
      {/* ── Toast notification ──────────────────────────────── */}
      {toast && (
        <aside className="app-toast" role="status" aria-live="polite">
          <span>{toast.message}</span>
          {toast.actionLink && (
            <Link to={toast.actionLink} className="toast-action-btn">
              {toast.actionText}
            </Link>
          )}
          <button
            className="toast-close-btn"
            onClick={() => setToast(null)}
            aria-label="Close notification"
          >
            ✕
          </button>
        </aside>
      )}

      {/* ── Section A — Hero ─────────────────────────────────── */}
      <section className="page-intro" aria-labelledby="replacements-heading">
        <div style={{ maxWidth: "var(--max-w-content)", margin: "0 auto" }}>
          <span className="eyebrow">Smart Sustainable Alternatives</span>
          <h1 id="replacements-heading">
            Find a <em>better alternative.</em>
          </h1>
          <p>
            Discover thoughtful replacements for everyday products. Compare materials,
            prices, and sustainability evidence before you switch.
          </p>

          {/* Prominent Search bar */}
          <div className="replacements-search-bar" role="search">
            <span className="search-icon" aria-hidden="true">⌕</span>
            <input
              type="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search for a product you want to replace by name, brand, category, or material…"
              aria-label="Search for a product you want to replace"
              className="replacements-search-input"
            />
            {searchTerm && (
              <button
                type="button"
                className="search-clear-btn"
                onClick={() => setSearchTerm("")}
                aria-label="Clear search input"
              >
                ✕ Clear
              </button>
            )}
          </div>
        </div>
      </section>

      <div className="section-wrap">
        {/* ── Section B — Category selection ───────────────────── */}
        <section aria-labelledby="category-filter-heading" className="replacements-category-section">
          <h2 id="category-filter-heading" className="sr-only">
            Filter by category
          </h2>
          <div className="category-pills" role="group" aria-label="Filter products by category">
            <button
              className={`category-pill${selectedCategory === "All" ? " active" : ""}`}
              onClick={() => setSelectedCategory("All")}
              aria-pressed={selectedCategory === "All"}
            >
              All Categories
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                className={`category-pill${selectedCategory === cat.name ? " active" : ""}`}
                onClick={() => setSelectedCategory(cat.name)}
                aria-pressed={selectedCategory === cat.name}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </section>

        {/* ── Section C — Select a product to replace ─────────── */}
        <section aria-labelledby="select-product-heading" className="replacements-select-section">
          <div className="section-header" style={{ marginBottom: "var(--space-4)" }}>
            <div className="section-header-text">
              <h2 id="select-product-heading">Select a product to replace</h2>
              <p>
                Choose a conventional product from the catalogue below to view its verified sustainable replacements.
              </p>
            </div>
            {selectedProduct && (
              <button
                className="secondary-button"
                onClick={handleClearSelection}
                style={{ fontSize: 13, padding: "8px 14px" }}
              >
                ✕ Deselect product
              </button>
            )}
          </div>

          {/* Persistent Selected Product Panel (when selected) */}
          {selectedProduct && (
            <div className="selected-product-banner" role="region" aria-label="Currently selected product">
              <div className="selected-product-badge">Selected for replacement</div>
              <div className="selected-product-content">
                <div className="selected-product-visual">
                  {selectedProduct.image_url ? (
                    <img src={selectedProduct.image_url} alt={selectedProduct.name} />
                  ) : (
                    <span className="visual-fallback-emoji" aria-hidden="true">📦</span>
                  )}
                </div>
                <div className="selected-product-details">
                  <span className="selected-cat-tag">{getCategoryName(selectedProduct)}</span>
                  <h3 className="selected-prod-title">{selectedProduct.name}</h3>
                  <p className="selected-prod-brand">{selectedProduct.brand || "Brand unavailable"}</p>
                  <p className="selected-prod-materials">
                    <strong>Current Composition:</strong> {selectedProduct.materials || "Standard conventional materials"}
                  </p>
                </div>
                <div className="selected-product-actions">
                  <div className="selected-prod-price">{formatPrice(selectedProduct.price, selectedProduct.currency)}</div>
                  <button
                    className="secondary-button change-selection-btn"
                    onClick={handleClearSelection}
                  >
                    Change product
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Conventional Products Grid */}
          {loadingProducts ? (
            <LoadingSkeleton count={4} />
          ) : errorProducts ? (
            <div className="no-results" role="alert">
              <div className="no-results-icon">⚠️</div>
              <h3>Unable to load catalogue</h3>
              <p>{errorProducts}</p>
              <button className="primary-button" onClick={() => window.location.reload()}>
                Try again
              </button>
            </div>
          ) : conventionalProducts.length === 0 ? (
            <div className="no-results" role="status">
              <div className="no-results-icon">🔍</div>
              <h3>No matching conventional products</h3>
              <p>Try searching for a different item name, brand, or choosing another category.</p>
              <button
                className="primary-button"
                onClick={() => {
                  setSearchTerm("");
                  setSelectedCategory("All");
                }}
              >
                Reset filters
              </button>
            </div>
          ) : (
            <div className="conventional-product-grid" role="radiogroup" aria-label="Conventional products to replace">
              {conventionalProducts.map((p) => {
                const isSelected = selectedProduct && selectedProduct.id === p.id;
                return (
                  <div
                    key={p.id}
                    className={`selectable-product-card${isSelected ? " selected" : ""}`}
                    onClick={() => handleSelectProduct(p)}
                    role="radio"
                    aria-checked={isSelected}
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        handleSelectProduct(p);
                      }
                    }}
                  >
                    <div className="selectable-card-header">
                      <span className="selectable-card-category">{getCategoryName(p)}</span>
                      <span className={`selection-indicator${isSelected ? " active" : ""}`} aria-hidden="true">
                        {isSelected ? "✓ Selected" : "+ Select"}
                      </span>
                    </div>

                    <div className="selectable-card-visual">
                      {p.image_url ? (
                        <img src={p.image_url} alt={p.name} loading="lazy" />
                      ) : (
                        <span className="visual-fallback-emoji" aria-hidden="true">📦</span>
                      )}
                    </div>

                    <div className="selectable-card-info">
                      <h4>{p.name}</h4>
                      <p className="selectable-brand">{p.brand || "Brand unavailable"}</p>
                      <p className="selectable-materials">
                        <span>Materials:</span> {p.materials || "Standard conventional composition"}
                      </p>
                      <div className="selectable-price">{formatPrice(p.price, p.currency)}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

        {/* ── Section D & E — Available Replacements Discovery ─── */}
        {selectedProduct && (
          <section
            aria-labelledby="alternatives-heading"
            className="replacements-results-section"
            style={{ marginTop: "var(--space-8)" }}
          >
            <div className="section-header">
              <div className="section-header-text">
                <span className="eyebrow" style={{ color: "var(--clr-primary)" }}>Verified Alternatives</span>
                <h2 id="alternatives-heading">
                  Sustainable replacements for {selectedProduct.name}
                </h2>
                <p>
                  Review genuine alternatives with verified composition changes, transparent pricing, and documented evidence.
                </p>
              </div>
            </div>

            {loadingReplacements ? (
              <LoadingSkeleton count={2} />
            ) : errorReplacements ? (
              <div className="no-results" role="alert">
                <div className="no-results-icon">⚠️</div>
                <h3>Could not load alternatives</h3>
                <p>{errorReplacements}</p>
              </div>
            ) : replacements.length === 0 ? (
              <div className="no-results" role="status">
                <div className="no-results-icon">🌿</div>
                <h3>No alternatives are currently available for this product.</h3>
                <p>
                  Our team is actively auditing Indian sustainable brands to identify verified replacements for this category.
                </p>
                <Link to="/products" className="primary-button" style={{ marginTop: "var(--space-4)" }}>
                  Browse full catalogue →
                </Link>
              </div>
            ) : (
              <div className="replacements-grid">
                {replacements.map((rep) => {
                  const alt = rep.replacement_product;
                  const isActive = activeReplacement && activeReplacement.id === rep.id;
                  const evidenceBadge = getEvidenceBadge(alt);
                  const sourceMeta = getSourceMeta(alt.source_verification_status, alt.purchase_url);

                  /* Price comparison calculation */
                  const hasBothPrices =
                    selectedProduct.price !== null &&
                    selectedProduct.price !== undefined &&
                    alt.price !== null &&
                    alt.price !== undefined;
                  const priceDiff = hasBothPrices ? Number(alt.price) - Number(selectedProduct.price) : null;

                  return (
                    <article
                      key={rep.id}
                      className={`replacement-card${isActive ? " active-replacement" : ""}`}
                    >
                      {/* Card Header & Type Badge */}
                      <div className="replacement-card-header">
                        <span className={`replacement-type-pill ${getReplacementTypeClass(rep.replacement_type)}`}>
                          {formatReplacementType(rep.replacement_type)}
                        </span>
                        <span className={`evidence-badge ${evidenceBadge.className}`} title={evidenceBadge.title}>
                          {evidenceBadge.label}
                        </span>
                      </div>

                      {/* Main visual & product titles */}
                      <div className="replacement-card-body">
                        <div className="replacement-visual">
                          {alt.image_url ? (
                            <img src={alt.image_url} alt={alt.name} loading="lazy" />
                          ) : (
                            <span className="visual-fallback-emoji" aria-hidden="true">🌿</span>
                          )}
                        </div>

                        <div className="replacement-main-details">
                          <h3>{alt.name}</h3>
                          <p className="replacement-brand">{alt.brand || "Brand unavailable"}</p>

                          {/* Price & Price comparison difference */}
                          <div className="price-comparison-box">
                            <div className="replacement-price-tag">
                              {formatPrice(alt.price, alt.currency)}
                            </div>
                            <div className="price-difference-indicator">
                              {hasBothPrices ? (
                                priceDiff > 0 ? (
                                  <span className="price-diff more-expensive">
                                    +₹{Math.abs(priceDiff).toFixed(0)} (More expensive)
                                  </span>
                                ) : priceDiff < 0 ? (
                                  <span className="price-diff less-expensive">
                                    -₹{Math.abs(priceDiff).toFixed(0)} (Less expensive)
                                  </span>
                                ) : (
                                  <span className="price-diff same-price">
                                    Same price (₹{Number(alt.price).toFixed(0)})
                                  </span>
                                )
                              ) : (
                                <span className="price-diff unavailable">
                                  Price comparison unavailable
                                </span>
                              )}
                            </div>
                          </div>

                          {/* Sustainability score bar */}
                          <div className="replacement-score-row">
                            <span className="score-label">Sustainability Score:</span>
                            <span className="score-val">
                              {alt.overall_sustainability_score !== null && alt.overall_sustainability_score !== undefined
                                ? `${Number(alt.overall_sustainability_score).toFixed(1)}/100`
                                : "Not rated"}
                            </span>
                          </div>
                          {alt.overall_sustainability_score !== null && alt.overall_sustainability_score !== undefined && (
                            <div className="score-track" style={{ marginBottom: 12 }}>
                              <div
                                className="score-fill"
                                style={{ width: `${Math.min(100, Math.max(0, alt.overall_sustainability_score))}%` }}
                              />
                            </div>
                          )}

                          {/* Material composition summary */}
                          <div className="replacement-materials-box">
                            <strong>Sustainable Composition:</strong> {alt.materials || "Natural eco-friendly composition"}
                          </div>

                          {/* Main Change description */}
                          <div className="replacement-change-summary">
                            <strong>Key Switch:</strong> {rep.main_change}
                          </div>

                          {/* Reason */}
                          <p className="replacement-reason-snippet">
                            <em>&ldquo;{rep.reason}&rdquo;</em>
                          </p>

                          {/* Source Link */}
                          <div className="replacement-source-row">
                            {sourceMeta ? (
                              <a
                                href={alt.purchase_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="source-link"
                                title={sourceMeta.title}
                              >
                                {sourceMeta.label}
                              </a>
                            ) : (
                              <span className="source-unavailable">Source unavailable</span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Card Actions: View details & Compare */}
                      <div className="replacement-card-footer">
                        <button
                          type="button"
                          className="secondary-button"
                          style={{ fontSize: 13 }}
                          onClick={() => handleViewExplanation(rep)}
                        >
                          View explanation ↓
                        </button>

                        <button
                          type="button"
                          className="primary-button"
                          style={{ fontSize: 13 }}
                          onClick={() => handleCompare(rep)}
                        >
                          + Compare with original
                        </button>
                      </div>
                    </article>
                  );
                })}
              </div>
            )}

            {/* ── Section F — Replacement Explanation Panel ─────────── */}
            {activeReplacement && (
              <div
                ref={explanationRef}
                className="explanation-panel"
                role="region"
                aria-labelledby="explanation-heading"
                style={{ marginTop: "var(--space-8)" }}
              >
                <div className="explanation-header">
                  <span className="eyebrow" style={{ color: "var(--clr-primary)" }}>Detailed Evaluation</span>
                  <h3 id="explanation-heading">
                    {selectedProduct.name} → {activeReplacement.replacement_product.name}
                  </h3>
                  <p className="explanation-type-badge">
                    Type: {formatReplacementType(activeReplacement.replacement_type)}
                  </p>
                </div>

                <div className="explanation-grid">
                  {/* 1. What changes? */}
                  <div className="explanation-card">
                    <div className="explanation-card-icon" aria-hidden="true">🔄</div>
                    <h4>What changes?</h4>
                    <p className="explanation-content-text">
                      {activeReplacement.main_change}
                    </p>
                  </div>

                  {/* 2. Why consider this replacement? */}
                  <div className="explanation-card">
                    <div className="explanation-card-icon" aria-hidden="true">🌱</div>
                    <h4>Why consider this replacement?</h4>
                    <p className="explanation-content-text">
                      {activeReplacement.reason}
                    </p>
                  </div>

                  {/* 3. What stays the same? */}
                  {(() => {
                    const shared = getSharedProperties(
                      selectedProduct,
                      activeReplacement.replacement_product
                    );
                    if (!shared) return null;
                    return (
                      <div className="explanation-card">
                        <div className="explanation-card-icon" aria-hidden="true">⚖️</div>
                        <h4>What stays the same?</h4>
                        <ul className="explanation-list">
                          {shared.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    );
                  })()}

                  {/* 4. What should you know? */}
                  <div className="explanation-card">
                    <div className="explanation-card-icon" aria-hidden="true">⚠️</div>
                    <h4>What should you know?</h4>
                    {activeReplacement.known_limitations ? (
                      <p className="explanation-content-text">
                        {activeReplacement.known_limitations}
                      </p>
                    ) : (
                      <p className="explanation-content-text" style={{ fontStyle: "italic", color: "var(--clr-text-muted)" }}>
                        No known trade-offs or disposal limitations documented.
                      </p>
                    )}

                    <div className="explanation-evidence-status">
                      <strong>Audit Status:</strong>{" "}
                      {activeReplacement.replacement_product.evidence_coverage > 0
                        ? `${Math.round(activeReplacement.replacement_product.evidence_coverage)}% verified third-party evidence.`
                        : "Manufacturer-reported data without independent third-party audit."}
                    </div>
                  </div>
                </div>

                {/* Direct Compare Trigger */}
                <div className="explanation-footer-actions">
                  <button
                    className="primary-button"
                    onClick={() => handleCompare(activeReplacement)}
                  >
                    Compare both products side-by-side →
                  </button>
                </div>
              </div>
            )}
          </section>
        )}

        {/* ── Comparison Tray / Sticky Bar (when products selected) ── */}
        {selectedProducts.length > 0 && (
          <aside className="replacements-compare-tray" aria-label="Comparison Tray">
            <div className="compare-tray-content">
              <span className="compare-tray-count">
                <strong>{selectedProducts.length} of 3</strong> products queued for comparison
              </span>
              <div className="compare-tray-actions">
                <button
                  className="secondary-button"
                  style={{ padding: "6px 12px", fontSize: 12 }}
                  onClick={() => setSelectedProducts([])}
                >
                  Clear comparison
                </button>
                <Link
                  to="/compare"
                  className="primary-button"
                  style={{ padding: "8px 16px", fontSize: 13 }}
                >
                  View comparison table →
                </Link>
              </div>
            </div>
          </aside>
        )}
      </div>
    </main>
  );
}

export default Replacements;
