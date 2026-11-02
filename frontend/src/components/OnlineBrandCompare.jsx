import { useState, useEffect } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

const SCORE_COLORS = {
  a: "#1e7e34", // Dark green
  b: "#28a745", // Green
  c: "#ffc107", // Yellow / amber
  d: "#fd7e14", // Orange
  e: "#dc3545", // Red
  "not-applicable": "#6c757d",
};

const NOVA_COLORS = {
  1: "#1e7e34",
  2: "#17a2b8",
  3: "#fd7e14",
  4: "#dc3545",
};

export default function OnlineBrandCompare() {
  const [quickPairs, setQuickPairs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedItems, setSelectedItems] = useState([
    "Tata Salt",
    "Patanjali Rock Salt",
  ]);
  const [comparisonMatrix, setComparisonMatrix] = useState(null);
  const [loadingCompare, setLoadingCompare] = useState(false);
  const [error, setError] = useState("");

  // Fetch quick pairs on mount
  useEffect(() => {
    async function loadQuickPairs() {
      try {
        const res = await fetch(`${API_BASE}/external-compare/quick-pairs`);
        if (res.ok) setQuickPairs(await res.json());
      } catch (_) {}
    }
    loadQuickPairs();
  }, []);

  // Run comparison whenever selectedItems change
  useEffect(() => {
    if (!selectedItems || selectedItems.length === 0) return;

    let cancelled = false;
    async function runCompare() {
      setLoadingCompare(true);
      setError("");
      try {
        const res = await fetch(`${API_BASE}/external-compare/compare`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ queries_or_barcodes: selectedItems }),
        });
        if (!res.ok) throw new Error("Comparison request failed");
        const data = await res.json();
        if (!cancelled) setComparisonMatrix(data);
      } catch (err) {
        if (!cancelled) setError("Could not fetch comparison data. Check backend.");
      } finally {
        if (!cancelled) setLoadingCompare(false);
      }
    }

    runCompare();
    return () => {
      cancelled = true;
    };
  }, [selectedItems]);

  // Live search handler
  async function handleSearch(e) {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const res = await fetch(
        `${API_BASE}/external-compare/search?query=${encodeURIComponent(
          searchQuery.trim()
        )}&page_size=6`
      );
      if (res.ok) {
        setSearchResults(await res.json());
      }
    } catch (_) {
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  }

  function addProductToCompare(productName) {
    if (selectedItems.includes(productName)) return;
    if (selectedItems.length >= 4) {
      alert("You can compare up to 4 products at once. Remove one first.");
      return;
    }
    setSelectedItems((prev) => [...prev, productName]);
    setSearchResults([]);
    setSearchQuery("");
  }

  function removeItem(index) {
    setSelectedItems((prev) => prev.filter((_, idx) => idx !== index));
  }

  function ScoreBadge({ score, type }) {
    if (!score) {
      return <span className="score-badge badge-na">N/A</span>;
    }
    const letter = score.toUpperCase();
    const bg = SCORE_COLORS[score.toLowerCase()] || "#6c757d";
    return (
      <span
        className="score-badge"
        style={{
          backgroundColor: bg,
          color: letter === "C" ? "#000" : "#fff",
        }}
        title={`${type}: Grade ${letter}`}
      >
        {letter}
      </span>
    );
  }

  function NovaBadge({ group }) {
    if (!group) return <span className="score-badge badge-na">N/A</span>;
    const bg = NOVA_COLORS[group] || "#6c757d";
    return (
      <span
        className="score-badge"
        style={{ backgroundColor: bg, color: "#fff" }}
        title={`NOVA Group ${group}`}
      >
        NOVA {group}
      </span>
    );
  }

  function NutrientPill({ label, val }) {
    if (!val) return null;
    const isHigh = val === "high";
    const isLow = val === "low";
    const bg = isHigh ? "#ffebee" : isLow ? "#e8f5e9" : "#fff3e0";
    const col = isHigh ? "#c62828" : isLow ? "#2e7d32" : "#ef6c00";
    return (
      <span
        style={{
          display: "inline-block",
          padding: "3px 8px",
          margin: "2px",
          borderRadius: "12px",
          fontSize: "11px",
          fontWeight: "600",
          backgroundColor: bg,
          color: col,
          textTransform: "capitalize",
        }}
      >
        {label}: {val}
      </span>
    );
  }

  return (
    <div className="online-brand-compare">
      {/* ── Subheader ─────────────────────────────────────── */}
      <div className="obc-header">
        <span className="eyebrow">🌐 Powered by Open Food Facts</span>
        <h2>Live Online Brand Comparison</h2>
        <p>
          Compare similar grocery products from different Indian brands side-by-side to
          instantly verify which option is <strong>healthier</strong> (Nutri-Score, NOVA group)
          and which is <strong>more eco-friendly</strong> (Eco-Score / Green-Score).
        </p>
      </div>

      {/* ── Quick-Comparison Preset Pills ─────────────────── */}
      <div className="obc-presets">
        <span className="obc-presets-title">⚡ Quick Comparisons:</span>
        <div className="obc-preset-pills">
          {quickPairs.map((pair, idx) => (
            <button
              key={idx}
              className="preset-pill-btn"
              onClick={() => setSelectedItems(pair.products)}
              title={`Compare ${pair.products.join(" vs ")}`}
            >
              {pair.title}
            </button>
          ))}
        </div>
      </div>

      {/* ── Search Bar to Add Custom Products ────────────── */}
      <div className="obc-search-wrap">
        <form className="obc-search-form" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search any online product/brand (e.g. Amul Butter, Dabur Honey, Tata Salt)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="primary-button" disabled={isSearching}>
            {isSearching ? "Searching..." : "🔍 Search Online"}
          </button>
        </form>

        {/* Live Search Results Dropdown */}
        {searchResults.length > 0 && (
          <div className="obc-search-dropdown">
            <div className="obc-dropdown-header">
              <span>Matching Online Products:</span>
              <button
                className="btn-text-danger"
                onClick={() => setSearchResults([])}
              >
                ✕ Close
              </button>
            </div>
            {searchResults.map((prod) => (
              <div key={prod.barcode} className="obc-dropdown-item">
                <div className="obc-dropdown-img">
                  {prod.image_url ? (
                    <img src={prod.image_url} alt={prod.name} />
                  ) : (
                    <span>📦</span>
                  )}
                </div>
                <div className="obc-dropdown-info">
                  <strong>{prod.name}</strong>
                  <span className="obc-dropdown-brand">{prod.brand}</span>
                  <div className="obc-dropdown-badges">
                    <span>
                      Nutri: <ScoreBadge score={prod.nutri_score} type="Nutri" />
                    </span>
                    <span>
                      Eco: <ScoreBadge score={prod.eco_score} type="Eco" />
                    </span>
                    <span>
                      <NovaBadge group={prod.nova_group} />
                    </span>
                  </div>
                </div>
                <button
                  className="secondary-button"
                  onClick={() => addProductToCompare(prod.name)}
                  disabled={selectedItems.includes(prod.name)}
                >
                  {selectedItems.includes(prod.name) ? "✓ Added" : "+ Add to Compare"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Active Selection Pills ────────────────────────── */}
      <div className="obc-selected-row">
        <span>Comparing ({selectedItems.length}/4):</span>
        {selectedItems.map((name, i) => (
          <span key={i} className="obc-tag">
            {name}
            <button
              onClick={() => removeItem(i)}
              aria-label={`Remove ${name}`}
              className="obc-tag-remove"
            >
              ×
            </button>
          </span>
        ))}
      </div>

      {/* ── Loading & Error States ────────────────────────── */}
      {loadingCompare && (
        <div className="comparison-empty">
          <div className="comparison-empty-icon">⏳</div>
          <h3>Fetching live health & eco data...</h3>
          <p>Querying Open Food Facts API in real time.</p>
        </div>
      )}

      {error && !loadingCompare && (
        <div className="alert-error">{error}</div>
      )}

      {/* ── Winners & Summary Banner ──────────────────────── */}
      {comparisonMatrix && !loadingCompare && (
        <>
          <div className="obc-verdict-grid">
            <div className="verdict-card verdict-health">
              <span className="verdict-badge">🥗 Health Rating</span>
              <h3>Healthiest Choice</h3>
              <p className="verdict-lead">
                {comparisonMatrix.health_winner || "Evaluating..."}
              </p>
            </div>
            <div className="verdict-card verdict-eco">
              <span className="verdict-badge">🌱 Environmental Footprint</span>
              <h3>Most Eco-Friendly Choice</h3>
              <p className="verdict-lead">
                {comparisonMatrix.eco_winner || "Evaluating..."}
              </p>
            </div>
          </div>

          {comparisonMatrix.summary_notes.length > 0 && (
            <div className="obc-insights-box">
              <h4>📋 Key Nutritional & Environmental Takeaways:</h4>
              <ul>
                {comparisonMatrix.summary_notes.map((note, nIdx) => (
                  <li key={nIdx}>{note}</li>
                ))}
              </ul>
            </div>
          )}

          {/* ── Side-by-Side Comparison Table ──────────────── */}
          <div className="comparison-table-wrap" style={{ marginTop: "24px" }}>
            <table className="comparison-table">
              <thead>
                <tr>
                  <th scope="col" style={{ width: "220px" }}>Evaluation Criteria</th>
                  {comparisonMatrix.products.map((p, idx) => (
                    <th scope="col" key={idx}>
                      <div className="comparison-col-header">
                        {p.image_url ? (
                          <img
                            src={p.image_url}
                            alt={p.name}
                            className="comparison-product-image"
                          />
                        ) : (
                          <div className="comparison-product-icon">📦</div>
                        )}
                        <span>{p.name}</span>
                        <small>{p.brand}</small>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Nutri-Score Row */}
                <tr>
                  <th scope="row">
                    <strong>Nutri-Score</strong>
                    <br />
                    <small style={{ color: "var(--clr-text-secondary)" }}>
                      Nutritional quality (A to E)
                    </small>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <ScoreBadge score={p.nutri_score} type="Nutri-Score" />
                        <span style={{ fontSize: "12px", color: "var(--clr-text-secondary)" }}>
                          {p.nutri_score_label}
                        </span>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Eco-Score Row */}
                <tr>
                  <th scope="row">
                    <strong>Eco-Score</strong>
                    <br />
                    <small style={{ color: "var(--clr-text-secondary)" }}>
                      Life-cycle carbon & eco-impact
                    </small>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <ScoreBadge score={p.eco_score} type="Eco-Score" />
                        <span style={{ fontSize: "12px", color: "var(--clr-text-secondary)" }}>
                          {p.eco_score_label}
                        </span>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Food Processing Row */}
                <tr>
                  <th scope="row">
                    <strong>Food Processing</strong>
                    <br />
                    <small style={{ color: "var(--clr-text-secondary)" }}>
                      NOVA scale (1=natural, 4=ultra-processed)
                    </small>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <NovaBadge group={p.nova_group} />
                        <span style={{ fontSize: "12px", color: "var(--clr-text-secondary)" }}>
                          {p.nova_label}
                        </span>
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Nutrient Levels (Fat, Sugar, Salt) */}
                <tr>
                  <th scope="row">
                    <strong>Nutrient Warning Levels</strong>
                    <br />
                    <small style={{ color: "var(--clr-text-secondary)" }}>
                      WHO nutrient profile
                    </small>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i}>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                        <NutrientPill label="Fat" val={p.nutrient_levels.fat} />
                        <NutrientPill label="Sat. Fat" val={p.nutrient_levels.saturated_fat} />
                        <NutrientPill label="Sugars" val={p.nutrient_levels.sugars} />
                        <NutrientPill label="Salt" val={p.nutrient_levels.salt} />
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Ingredients */}
                <tr>
                  <th scope="row">
                    <strong>Ingredients & Additives</strong>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i} style={{ fontSize: "12px", lineHeight: 1.5 }}>
                      {p.ingredients || "Ingredients list not specified in public record."}
                    </td>
                  ))}
                </tr>

                {/* Packaging & Disposal */}
                <tr>
                  <th scope="row">
                    <strong>Packaging Material</strong>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i} style={{ fontSize: "12px", lineHeight: 1.5 }}>
                      {p.packaging || "Packaging details not catalogued."}
                    </td>
                  ))}
                </tr>

                {/* Source Link */}
                <tr>
                  <th scope="row">
                    <strong>Official Open Record</strong>
                  </th>
                  {comparisonMatrix.products.map((p, i) => (
                    <td key={i}>
                      <a
                        href={p.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-link"
                      >
                        Open Food Facts Record ↗
                      </a>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
