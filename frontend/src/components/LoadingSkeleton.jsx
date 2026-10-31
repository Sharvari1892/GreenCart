/**
 * LoadingSkeleton — Animated shimmer placeholder cards for loading states.
 * Props:
 *   count  {number} — number of skeleton cards to render (default 6)
 */
function LoadingSkeleton({ count = 6 }) {
  return (
    <div className="product-grid" aria-busy="true" aria-label="Loading products">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="skeleton-card" aria-hidden="true">
          <div className="skeleton-img skeleton" />
          <div className="skeleton-body">
            <div className="skeleton skeleton-line w-40" />
            <div className="skeleton skeleton-line w-80 h-20" />
            <div className="skeleton skeleton-line w-60" />
            <div className="skeleton skeleton-line w-100" />
            <div className="skeleton skeleton-line w-100" />
            <div className="skeleton skeleton-line w-60" style={{ marginTop: 12 }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export default LoadingSkeleton;
