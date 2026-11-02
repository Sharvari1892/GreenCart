# GreenCart API Documentation

## Base URL
Local Development: `http://127.0.0.1:8000/api`

## Authentication

Authentication is handled via JWT bearer tokens. Passwords are mathematically hashed with Argon2.

### 1. Register
- **URL**: `POST /auth/register`
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**: `200 OK` (User object) or `400 Bad Request` (Duplicate email)

### 2. Login
- **URL**: `POST /auth/login`
- **Request Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "refresh_token": "rT8z..."
  }
  ```

### 3. Refresh Token
- **URL**: `POST /auth/refresh`
- **Request Body**: `{"refresh_token": "rT8z..."}`
- **Response**: `200 OK` with new `access_token` and `refresh_token`

### 4. Logout
- **URL**: `POST /auth/logout`
- **Request Body**: `{"refresh_token": "rT8z..."}`
- **Response**: `200 OK`

### 5. Get Current User
- **URL**: `GET /auth/me`
- **Headers**: `Authorization: Bearer <access_token>`

---

## Products & Categories

### 1. Get Categories
- **URL**: `GET /categories`
- **Response**: List of category objects.

### 2. Get Products (with Pagination & Filtering)
- **URL**: `GET /products`
- **Query Params**:
  - `page` (default 1)
  - `page_size` (default 20, max 100)
  - `search` (name or brand)
  - `category_id`
  - `min_price`, `max_price`
  - `min_durability`, `min_packaging`, `min_repairability`
  - `sort_by` (name, price, durability_score, sustainability_score)
  - `sort_desc` (boolean)
- **Response Format**:
  ```json
  {
    "items": [...],
    "total": 50,
    "page": 1,
    "page_size": 20,
    "total_pages": 3
  }
  ```

### 3. Get Product Details
- **URL**: `GET /products/{id}`
- **Response**: Includes `category`, `evidence`, and `overall_sustainability_score`.

### 4. Get Product Evidence
- **URL**: `GET /products/{id}/evidence`
- **Response**: List of evidence objects.

---

## Wishlist (Requires Authentication)

### 1. Add to Wishlist
- **URL**: `POST /wishlists`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**: `{"product_id": 1}`

### 2. Get User Wishlists
- **URL**: `GET /wishlists`
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Params**: `skip` (default 0), `limit` (default 20)

### 3. Remove from Wishlist
- **URL**: `DELETE /wishlists/{product_id}`
- **Headers**: `Authorization: Bearer <access_token>`

---

## Comparisons (Requires Authentication)

### 1. Create Comparison
- **URL**: `POST /comparisons`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**: `{"product_ids": [1, 2, 3]}`
- **Rules**: Must provide 2 to 4 valid, distinct product IDs.

### 2. Get Comparison
- **URL**: `GET /comparisons/{id}`
- **Headers**: `Authorization: Bearer <access_token>`

---

## Admin APIs (Requires 'admin' Role)

All admin endpoints require an access token belonging to a user with `role="admin"`.

- **POST `/admin/products`**: Create a product.
- **PATCH `/admin/products/{id}`**: Update a product.
- **DELETE `/admin/products/{id}`**: Delete a product.
- **POST `/admin/evidence`**: Add evidence to a product. (Initial status is always 'pending').
- **PATCH `/admin/evidence/{id}`**: Update evidence details.
- **PATCH `/admin/evidence/{id}/verification`**: Update verification status (`pending`, `verified`, `rejected`).
  - Request body: `{"verification_status": "verified"}`
