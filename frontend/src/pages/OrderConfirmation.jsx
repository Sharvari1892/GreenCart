import { useLocation, Link, useParams } from "react-router-dom";

function formatINR(amount) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);
}

export default function OrderConfirmation() {
  const { state } = useLocation();
  const { orderId } = useParams();
  const order = state?.order;

  if (!order) {
    return (
      <main className="order-confirm-page">
        <div className="cart-empty">
          <h2>Order #{orderId}</h2>
          <p>Order details not available in this session.</p>
          <Link className="primary-button" to="/products">Continue Shopping</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="order-confirm-page">
      <div className="order-confirm-inner">
        <div className="order-success-icon">🎉</div>
        <h1>Order Confirmed!</h1>
        <p className="order-confirm-sub">
          Thank you, <strong>{order.shipping_name}</strong>! Your demo order <strong>#{order.id}</strong> has been placed.
        </p>
        <p className="order-confirm-note">
          A confirmation would be sent to <strong>{order.shipping_email}</strong>. This is a demo — no real order or email is created.
        </p>

        <div className="order-details-card">
          <div className="order-details-header">
            <span>Order #{order.id}</span>
            <span className="order-status-badge">{order.status}</span>
          </div>

          <div className="order-ship-info">
            <p><strong>Deliver to:</strong> {order.shipping_address}</p>
          </div>

          <div className="order-items-list">
            {order.items.map((item) => (
              <div key={item.id} className="order-item-row">
                <span>{item.product_name}</span>
                <span className="order-item-qty">×{item.quantity}</span>
                <span>{formatINR(item.subtotal)}</span>
              </div>
            ))}
          </div>

          <div className="order-total-row">
            <strong>Total Paid</strong>
            <strong>{formatINR(order.total_amount)}</strong>
          </div>
        </div>

        <div className="order-actions">
          <Link className="primary-button" to="/products">Continue Shopping</Link>
          <Link className="btn-outline" to="/">Go to Home</Link>
        </div>
      </div>
    </main>
  );
}
