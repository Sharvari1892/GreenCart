# 🌿 GreenCart — Sustainable Grocery E-Commerce & Brand Comparison Platform

> **A modern, full-stack e-commerce demonstration platform built with React, Vite, FastAPI, and an in-memory SQLite database.** Explore products from 15 iconic Indian brands, manage your shopping cart and mock checkout, and compare competing products side-by-side using live nutritional (**Nutri-Score**) and environmental (**Eco-Score / Green-Score**) metrics powered by Open Food Facts.

---

## ✨ Key Features

### 1. 🇮🇳 15 Famous Indian Brands Catalog
A rich demo catalog containing **60+ realistic products** across 8 categories:
- **Food & Staples:** Tata, Amul, Aashirvaad, Dabur, Patanjali
- **Personal & Baby Care:** Himalaya, Mamaearth, Forest Essentials, Khadi India
- **Sustainable Fashion & Textiles:** Fabindia, Khadi India
- **Home & Living:** Godrej, Asian Paints
- **Smart Tech & Audio:** boAt, Noise
- **Traditional Beverages & Snacks:** Paper Boat

Each product features pricing in INR (₹), high-resolution imagery, composition specifications, packaging ratings, and sustainability scores.

---

### 2. ⚡ Zero-Setup In-Memory Architecture (No PostgreSQL Required)
- **Database:** Runs purely in-memory using **SQLite (`sqlite:///:memory:`)** with SQLAlchemy's `StaticPool` and thread-safe connection pooling.
- **Auto-Initialization:** Database tables, schemas, relationships, demo users, categories, and all 60+ products are **automatically generated and seeded on backend startup**.
- **Self-Contained:** Zero Docker, PostgreSQL, or paid database server installation required. Perfect for instant faculty presentations and local code evaluation.
- *Note:* In-memory data resets when the backend server restarts.

---

### 3. 🌐 Live Online Brand Comparison (Open Food Facts Integration)
Directly compare similar products from competing brands to evaluate which is **healthier** and which is **more eco-friendly**:
- **Nutri-Score (A to E):** Standardized nutritional quality rating.
- **Eco-Score / Green-Score (A to E):** Life-cycle environmental impact, carbon footprint, and packaging recyclability.
- **NOVA Food Processing Group (1 to 4):** Flags whole foods (NOVA 1–2) vs. ultra-processed industrial items (NOVA 4).
- **Nutrient Warning Tags:** Highlights WHO thresholds for Fat, Saturated Fat, Sugar, and Salt.
- **AI-Powered Verdict Banners:** Automatically announces the **Health Winner** and **Eco Winner** with actionable takeaways.
- **Curated 1-Click Matchups:**
  - *Tata Salt* vs. *Patanjali Rock Salt*
  - *Amul Butter* vs. *Nutralite Table Spread*
  - *Dabur Honey* vs. *Patanjali Desi Honey*
  - *Tata Tea Gold* vs. *Red Label Natural Care*
  - *Aashirvaad Atta* vs. *Patanjali Chakki Atta*

---

### 4. 🛒 Complete E-Commerce Shopping Experience
- **Live Cart:** Add items from anywhere on the site with animated feedback, live badge counter in the sticky header, and persistent session support (`localStorage`).
- **Cart Management (`/cart`):** Inline quantity adjusters (+/−), item removal, clear-all action, and order subtotal calculations.
- **Mock Checkout (`/checkout`):** Shipping address validation and demo payment method selection (Cash on Delivery, UPI, Credit/Debit Card).
- **Order Confirmation (`/order-confirmation/:id`):** Receipt generation with unique Order IDs and breakdown.
- **Eco-Replacements (`/replacements`):** Discover greener alternatives for conventional everyday household products.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, React Router 6, Vanilla CSS Design System, Responsive Mobile Drawer |
| **Backend** | FastAPI, Uvicorn, SQLAlchemy 2.x, Pydantic v2, HTTPX |
| **Database** | SQLite In-Memory (`sqlite:///:memory:`) with `StaticPool` |
| **External APIs** | Open Food Facts REST API (v2) |

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### 1. Start the FastAPI Backend

Open a terminal in the project directory:

```bash
cd backend

# Create and activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Backend API URL:** `http://127.0.0.1:8000`
- **Interactive Swagger Documentation:** `http://127.0.0.1:8000/docs`
- On startup, the terminal will confirm:
  ```
  [GreenCart] Demo database seeded: 8 categories, 63 products.
  ```

---

### 2. Start the React Frontend

Open a second terminal:

```bash
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```

- **Frontend Web App:** `http://localhost:5173`

---

## 📁 Project Structure

```text
GreenCart/
├── README.md                      # Root documentation
├── backend/
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment configuration (SQLite in-memory)
│   └── app/
│       ├── main.py                # FastAPI app entry point & lifespan startup
│       ├── core/
│       │   └── config.py          # App settings & SQLite configuration
│       ├── db/
│       │   ├── session.py         # SQLAlchemy engine & StaticPool setup
│       │   ├── base.py            # Model registry
│       │   └── seed.py            # 15 Indian brands & 60+ product demo seeder
│       ├── models/
│       │   ├── product.py         # Product model & score constraints
│       │   ├── category.py        # Category model
│       │   ├── user.py            # User authentication model
│       │   └── cart_order.py      # CartItem, Order, OrderItem models
│       ├── schemas/               # Pydantic validation schemas
│       ├── repositories/          # Data access layer
│       └── api/
│           ├── deps.py            # DB session & auth dependencies
│           └── endpoints/
│               ├── products.py         # Product catalog & filter API
│               ├── categories.py       # Category listing API
│               ├── cart.py             # Shopping cart endpoints
│               ├── orders.py           # Checkout & order history API
│               └── external_compare.py # Open Food Facts live comparison API
└── frontend/
    ├── package.json               # Frontend dependencies & scripts
    ├── vite.config.js             # Vite configuration
    └── src/
        ├── App.jsx                # Router, CartProvider & layout
        ├── App.css                # GreenCart design system styling
        ├── context/
        │   └── CartContext.jsx    # Global cart state & session manager
        ├── components/
        │   ├── Navbar.jsx         # Sticky header with live cart badge
        │   ├── ProductCard.jsx    # Card with "Add to Cart" & "+ Compare"
        │   └── OnlineBrandCompare.jsx # Open Food Facts live comparison UI
        └── pages/
            ├── Home.jsx           # Landing page with hero & categories
            ├── Products.jsx       # Catalog browsing, search & filters
            ├── Cart.jsx           # Shopping cart page
            ├── Checkout.jsx       # Delivery form & payment method selection
            ├── OrderConfirmation.jsx # Order receipt page
            ├── Compare.jsx        # Dual-mode comparison engine
            ├── Replacements.jsx   # Greener alternative recommendations
            └── About.jsx          # Mission, values & methodology
```

---

## 👥 Demo User Credentials

The database automatically initializes two demo accounts:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@greencart.demo` | `Admin@123` |
| **Customer** | `priya@greencart.demo` | `User@123` |

*(Guest checkout is enabled by default—users can add to cart and checkout without signing in).*

---

## 🛡️ License & Academic Notice
This project is developed for educational and demonstration purposes. All product names, trademarks, and logos belong to their respective brand owners and are referenced solely for academic comparative evaluation under fair use.
