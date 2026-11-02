/**
 * CartContext — manages the GreenCart shopping cart using the backend /api/cart API.
 * Session ID is persisted in localStorage so the cart survives page refreshes.
 * NOTE: The backend uses SQLite in-memory, so cart data resets when the server restarts.
 */
import { createContext, useContext, useState, useEffect, useCallback } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

function getSessionId() {
  let sid = localStorage.getItem("greencart_session");
  if (!sid) {
    sid = crypto.randomUUID();
    localStorage.setItem("greencart_session", sid);
  }
  return sid;
}

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ session_id: "", items: [], total: 0, item_count: 0 });
  const [loading, setLoading] = useState(false);

  const sessionId = getSessionId();
  const headers = { "Content-Type": "application/json", "X-Session-Id": sessionId };

  const fetchCart = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/cart`, { headers: { "X-Session-Id": sessionId } });
      if (res.ok) setCart(await res.json());
    } catch (_) { /* backend may be starting */ }
  }, [sessionId]);

  useEffect(() => { fetchCart(); }, [fetchCart]);

  async function addToCart(productId, quantity = 1) {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/cart`, {
        method: "POST",
        headers,
        body: JSON.stringify({ product_id: productId, quantity }),
      });
      if (res.ok) setCart(await res.json());
    } finally { setLoading(false); }
  }

  async function updateItem(itemId, quantity) {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/cart/${itemId}`, {
        method: "PUT",
        headers,
        body: JSON.stringify({ quantity }),
      });
      if (res.ok) setCart(await res.json());
    } finally { setLoading(false); }
  }

  async function removeItem(itemId) {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/cart/${itemId}`, { method: "DELETE", headers });
      if (res.ok) setCart(await res.json());
    } finally { setLoading(false); }
  }

  async function clearCart() {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/cart`, { method: "DELETE", headers });
      if (res.ok) setCart(await res.json());
    } finally { setLoading(false); }
  }

  return (
    <CartContext.Provider value={{ cart, loading, addToCart, updateItem, removeItem, clearCart, sessionId, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}
