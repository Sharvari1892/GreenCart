import { useState } from "react";
import { useCart } from "../context/CartContext";

/** Background variant classes cycle through 5 colour palettes */
const BG_VARIANTS = ["var-a", "var-b", "var-c", "var-d", "var-e"];

/**
 * Format price in INR (₹) using Intl.NumberFormat.
 * Gracefully handles missing prices and falls back to currency symbol.
 */
function formatPrice(product) {
  if (product.price === null || product.price === undefined) {
    return "Price unavailable";
  }
  const currency = product.currency || "INR";
  try {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(Number(product.price));
  } catch {
    return `₹${product.price}`;
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
  const { addToCart } = useCart();
  const [addedFeedback, setAddedFeedback] = useState(false);

  const score = product.overall_sustainability_score;
  const hasScore =
    score !== null &&
    score !== undefined &&
    score !== "" &&
    Number.isFinite(Number(score));

  const bgVariant = BG_VARIANTS[(product.id - 1) % BG_VARIANTS.length];
  const isSustainable = Boolean(product.is_sustainable);

  const evidenceBadge = (() => {
    const coverage = Number(product.evidence_coverage) || 0;
    if (coverage >= 60) {
      return {
        className: "verified",
        label: "✓ Verified Evidence",
        title: `${Math.round(coverage)}% independently certified evidence`,
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
  })();

  const sourceMeta = (() => {
    if (!product.purchase_url) return null;
    const status = product.source_verification_status;
    if (status === "verified_exact_source") {
      return { label: "Verified Store ↗", title: "Direct purchase page from verified merchant/brand store" };
    }
    if (status === "manufacturer_info_only") {
      return { label: "Manufacturer Info ↗", title: "Manufacturer official catalogue/specifications (not a direct store)" };
    }
    if (status === "retailer_source") {
      return { label: "Retailer Listing ↗", title: "Third-party retailer / marketplace listing" };
    }
    return { label: "Reference Source ↗", title: "Regulatory reference or unverified source" };
  })();

  async function handleAddToCart() {
    await addToCart(product.id, 1);
    setAddedFeedback(true);
    setTimeout(() => setAddedFeedback(false), 1500);
  }

  return (
    <article className={`product-card ${isSustainable ? "card-sustainable" : "card-conventional"}`}>
      {/* ── Image area ────────────────────────────────────── */}
      <div className={`product-visual ${bgVariant}`}>
        {/* Conventional vs Sustainable Alternative Tag */}
        <span className={`product-type-badge ${isSustainable ? "type-sustainable" : "type-conventional"}`}>
          {isSustainable ? "🌱 Sustainable Alternative" : "Conventional Product"}
        </span>

        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            loading="lazy"
            onError={(e) => {
              e.currentTarget.style.display = "none";
              const fallback = e.currentTarget.parentElement.querySelector(".product-visual-emoji");
              if (fallback) fallback.style.display = "block";
            }}
          />
        ) : null}

        {/* Fallback visual — shown when no image or image fails to load */}
        <span
          className="product-visual-emoji"
          aria-hidden="true"
          style={{ display: product.image_url ? "none" : "block" }}
        >
          {isSustainable ? "🌿" : "📦"}
        </span>

        <button
          className={`compare-toggle${isSelected ? " chosen" : ""}`}
          onClick={() => onToggleCompare(product.id)}
          aria-label={`${isSelected ? "Remove" : "Add"} ${product.name} ${isSelected ? "from" : "to"} comparison`}
          aria-pressed={isSelected}
          title={isSelected ? "Remove from comparison" : "Add to comparison"}
        >
          {isSelected ? "✓" : "+"}
        </button>
      </div>

      {/* ── Info area ─────────────────────────────────────── */}
      <div className="product-info">
        <div className="product-category-row">
          <span className="product-category-badge">{categoryName}</span>
          <span className={`evidence-badge ${evidenceBadge.className}`} title={evidenceBadge.title}>
            {evidenceBadge.label}
          </span>
        </div>

        <h3>{product.name}</h3>
        {product.brand && (
          <p className="product-brand">{product.brand}</p>
        )}

        <p className="product-desc">
          {product.description || "Product details unavailable."}
        </p>

        {/* Composition / Materials summary */}
        {product.materials && (
          <div className="product-materials-box">
            <span className="materials-label">Composition:</span>
            <span className="materials-text">{product.materials}</span>
          </div>
        )}

        {/* Sustainability score bar */}
        <div className="eco-score">
          <div className="eco-score-row">
            <span>Sustainability score</span>
            <strong>
              {hasScore ? `${Number(score).toFixed(1)}/100` : "Not rated"}
            </strong>
          </div>
          <div
            className="score-track"
            role="progressbar"
            aria-valuenow={hasScore ? Math.round(score) : 0}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Sustainability score: ${hasScore ? score.toFixed(1) : "not rated"}`}
          >
            <div
              className={`score-fill ${!isSustainable ? "score-fill-low" : ""}`}
              style={{
                width: `${hasScore ? Math.min(100, Math.max(0, score)) : 0}%`,
              }}
            />
          </div>
        </div>

        {/* Footer: price + source link + compare button + cart button */}
        <div className="product-footer">
          <div className="product-pricing">
            <span className="product-price">{formatPrice(product)}</span>
            {sourceMeta ? (
              <a
                href={product.purchase_url}
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

          <div className="product-card-actions">
            <button
              className={`compare-button${isSelected ? " selected" : ""}`}
              onClick={() => onToggleCompare(product.id)}
              aria-pressed={isSelected}
            >
              {isSelected ? "✓ Selected" : "+ Compare"}
            </button>
            <button
              className={`add-to-cart-btn${addedFeedback ? " added" : ""}`}
              onClick={handleAddToCart}
              aria-label={`Add ${product.name} to cart`}
            >
              {addedFeedback ? "✓ Added!" : "🛒 Add to Cart"}
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}

export default ProductCard;
