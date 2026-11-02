import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

const API_BASE = "http://127.0.0.1:8000/api";

function formatINR(amount) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);
}

export default function Checkout() {
  const { cart, sessionId, fetchCart } = useCart();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", address: "", payment: "demo_cod" });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const { items, total } = cart;

  if (!items || items.length === 0) {
    return (
      <main className="checkout-page">
        <div className="cart-empty">
          <div className="cart-empty-icon">🛒</div>
          <h2>Nothing to checkout</h2>
          <Link className="primary-button" to="/products">Browse Products</Link>
        </div>
      </main>
    );
  }

  function validate() {
    const e = {};
    if (!form.name.trim()) e.name = "Full name is required";
    if (!form.email.trim() || !/\S+@\S+\.\S+/.test(form.email)) e.email = "Valid email is required";
    if (!form.address.trim() || form.address.trim().length < 10) e.address = "Please enter a complete delivery address";
    return e;
  }

  async function handleSubmit(ev) {
    ev.preventDefault();
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/orders`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Session-Id": sessionId },
        body: JSON.stringify({
          shipping_name: form.name,
          shipping_email: form.email,
          shipping_address: form.address,
          payment_method: form.payment,
        }),
      });
      if (res.ok) {
        const order = await res.json();
        await fetchCart(); // cart is now cleared on server
        navigate(`/order-confirmation/${order.id}`, { state: { order } });
      } else {
        const err = await res.json();
        setErrors({ general: err.detail || "Checkout failed. Please try again." });
      }
    } catch {
      setErrors({ general: "Could not reach server. Make sure the backend is running." });
    } finally {
      setSubmitting(false);
    }
  }

  function field(label, key, type = "text", placeholder = "") {
    return (
      <div className="form-field">
        <label htmlFor={key}>{label}</label>
        <input
          id={key}
          type={type}
          placeholder={placeholder}
          value={form[key]}
          onChange={(e) => { setForm(f => ({ ...f, [key]: e.target.value })); setErrors(er => ({ ...er, [key]: undefined })); }}
          className={errors[key] ? "input-error" : ""}
        />
        {errors[key] && <span className="field-error">{errors[key]}</span>}
      </div>
    );
  }

  return (
    <main className="checkout-page">
      <div className="checkout-inner">
        <h1>Checkout</h1>

        {errors.general && <div className="alert-error">{errors.general}</div>}

        <div className="checkout-layout">
          {/* Form */}
          <form className="checkout-form" onSubmit={handleSubmit} noValidate>
            <section className="form-section">
              <h2>Delivery Details</h2>
              {field("Full Name", "name", "text", "e.g. Priya Sharma")}
              {field("Email Address", "email", "email", "e.g. priya@example.com")}
              <div className="form-field">
                <label htmlFor="address">Delivery Address</label>
                <textarea
                  id="address"
                  rows={3}
                  placeholder="Street, City, State, PIN"
                  value={form.address}
                  onChange={(e) => { setForm(f => ({ ...f, address: e.target.value })); setErrors(er => ({ ...er, address: undefined })); }}
                  className={errors.address ? "input-error" : ""}
                />
                {errors.address && <span className="field-error">{errors.address}</span>}
              </div>
            </section>

            <section className="form-section">
              <h2>Payment Method</h2>
              <div className="payment-options">
                {[
                  { id: "demo_cod", label: "💵 Cash on Delivery (Demo)" },
                  { id: "demo_upi", label: "📱 UPI (Demo)" },
                  { id: "demo_card", label: "💳 Card (Demo)" },
                ].map((opt) => (
                  <label key={opt.id} className={`payment-option${form.payment === opt.id ? " selected" : ""}`}>
                    <input
                      type="radio"
                      name="payment"
                      value={opt.id}
                      checked={form.payment === opt.id}
                      onChange={() => setForm(f => ({ ...f, payment: opt.id }))}
                    />
                    {opt.label}
                  </label>
                ))}
              </div>
              <p className="payment-disclaimer">
                ⚠️ This is a demo. No real payment is processed.
              </p>
            </section>

            <button className="primary-button checkout-btn" type="submit" disabled={submitting}>
              {submitting ? "Placing Order…" : `Place Order · ${formatINR(total)}`}
            </button>
          </form>

          {/* Order summary */}
          <aside className="checkout-summary">
            <h2>Order Summary</h2>
            <div className="co-summary-items">
              {items.map((item) => (
                <div key={item.id} className="co-summary-row">
                  <span className="co-item-name">{item.product_name} <span className="co-qty">×{item.quantity}</span></span>
                  <span>{formatINR(item.subtotal)}</span>
                </div>
              ))}
            </div>
            <div className="co-total-row">
              <span>Total</span><strong>{formatINR(total)}</strong>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
