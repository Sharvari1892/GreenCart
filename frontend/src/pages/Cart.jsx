import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

function formatINR(amount) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);
}

export default function Cart() {
  const { cart, loading, updateItem, removeItem, clearCart } = useCart();
  const { items, total, item_count } = cart;

  if (!items || items.length === 0) {
    return (
      <main className="cart-page">
        <div className="cart-empty">
          <div className="cart-empty-icon">🛒</div>
          <h2>Your cart is empty</h2>
          <p>Add some products to get started!</p>
          <Link className="primary-button" to="/products">Browse Products</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="cart-page">
      <div className="cart-inner">
        <div className="cart-header-row">
          <h1>🛒 Shopping Cart <span className="cart-count-label">({item_count} items)</span></h1>
          <button className="btn-text-danger" onClick={clearCart} disabled={loading}>Clear all</button>
        </div>

        <div className="cart-layout">
          {/* Items list */}
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item-card">
                <div className="cart-item-img">
                  {item.product_image
                    ? <img src={item.product_image} alt={item.product_name} loading="lazy" />
                    : <span className="cart-item-emoji">📦</span>
                  }
                </div>
                <div className="cart-item-details">
                  <h3>{item.product_name}</h3>
                  {item.product_brand && <p className="cart-item-brand">{item.product_brand}</p>}
                  <p className="cart-item-price">{formatINR(item.product_price)} each</p>
                </div>
                <div className="cart-item-controls">
                  <div className="qty-control">
                    <button
                      onClick={() => updateItem(item.id, item.quantity - 1)}
                      disabled={loading}
                      aria-label="Decrease quantity"
                    >−</button>
                    <span className="qty-value">{item.quantity}</span>
                    <button
                      onClick={() => updateItem(item.id, item.quantity + 1)}
                      disabled={loading}
                      aria-label="Increase quantity"
                    >+</button>
                  </div>
                  <p className="cart-item-subtotal">{formatINR(item.subtotal)}</p>
                  <button
                    className="btn-remove"
                    onClick={() => removeItem(item.id)}
                    disabled={loading}
                    aria-label={`Remove ${item.product_name}`}
                  >✕</button>
                </div>
              </div>
            ))}
          </div>

          {/* Order summary */}
          <aside className="cart-summary">
            <h2>Order Summary</h2>
            <div className="summary-row"><span>Subtotal</span><strong>{formatINR(total)}</strong></div>
            <div className="summary-row"><span>Delivery</span><span className="free-tag">FREE (Demo)</span></div>
            <div className="summary-row summary-total"><span>Total</span><strong>{formatINR(total)}</strong></div>
            <Link className="primary-button checkout-btn" to="/checkout">
              Proceed to Checkout →
            </Link>
            <Link className="btn-outline" to="/products">← Continue Shopping</Link>
          </aside>
        </div>
      </div>
    </main>
  );
}
