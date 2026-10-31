/** Background variant classes cycle through 5 colour palettes */
const BG_VARIANTS = ["var-a", "var-b", "var-c", "var-d", "var-e"];

/**
 * Format price with Intl.NumberFormat.
 * Falls back to `<price> <currency>` string if an unsupported currency code is given.
 */
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

/**
 * ProductCard — reusable product card used on the Products page and home featured grid.
 *
 * Props:
 *   product          — product object from API
 *   categoryName     — resolved category display name string
 *   isSelected       — boolean, whether this product is in the compare selection
 *   onToggleCompare  — (productId) => void
 */
function ProductCard({ product, categoryName, isSelected, onToggleCompare }) {
  const score = product.overall_sustainability_score;
  const hasScore =
    score !== null &&
    score !== undefined &&
    score !== "" &&
    Number.isFinite(Number(score));

  const bgVariant = BG_VARIANTS[(product.id - 1) % BG_VARIANTS.length];

  return (
    <article className="product-card">
      {/* ── Image area ────────────────────────────────────── */}
      <div className={`product-visual ${bgVariant}`}>
        <span className="eco-tag">♻ Eco-scored</span>

        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            loading="lazy"
            onError={(e) => {
              e.currentTarget.style.display = "none";
              e.currentTarget.nextSibling.style.display = "block";
            }}
          />
        ) : null}

        {/* Emoji fallback — shown when no image or image fails to load */}
        <span
          className="product-visual-emoji"
          aria-hidden="true"
          style={{ display: product.image_url ? "none" : "block" }}
        >
          🌿
        </span>

        <button
          className={`compare-toggle${isSelected ? " chosen" : ""}`}
          onClick={() => onToggleCompare(product.id)}
          aria-label={`${isSelected ? "Remove" : "Add"} ${product.name} ${isSelected ? "from" : "to"} comparison`}
          aria-pressed={isSelected}
        >
          {isSelected ? "✓" : "+"}
        </button>
      </div>

      {/* ── Info area ─────────────────────────────────────── */}
      <div className="product-info">
        <span className="product-category-badge">{categoryName}</span>
        <h3>{product.name}</h3>
        {product.brand && (
          <p className="product-brand">{product.brand}</p>
        )}
        <p className="product-desc">
          {product.description || "Product details unavailable."}
        </p>

        {/* Sustainability score bar */}
        <div className="eco-score">
          <div className="eco-score-row">
            <span>Sustainability score</span>
            <strong>
              {hasScore ? `${Number(score).toFixed(1)}/100` : "Not rated"}
            </strong>
          </div>
          <div className="score-track" role="progressbar"
               aria-valuenow={hasScore ? Math.round(score) : 0}
               aria-valuemin={0} aria-valuemax={100}
               aria-label={`Sustainability score: ${hasScore ? score.toFixed(1) : "not rated"}`}>
            <div
              className="score-fill"
              style={{
                width: `${hasScore ? Math.min(100, Math.max(0, score)) : 0}%`,
              }}
            />
          </div>
        </div>

        {/* Footer: price + compare button */}
        <div className="product-footer">
          <div>
            <span className="product-price">{formatPrice(product)}</span>
          </div>
          <button
            className={`compare-button${isSelected ? " selected" : ""}`}
            onClick={() => onToggleCompare(product.id)}
            aria-pressed={isSelected}
          >
            {isSelected ? "✓ Selected" : "+ Compare"}
          </button>
        </div>
      </div>
    </article>
  );
}

export default ProductCard;
