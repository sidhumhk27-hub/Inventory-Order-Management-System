# Inventory & Order Management System

A full-stack inventory and order management system built with FastAPI, MySQL, and vanilla JS. Supports product/customer/category management, order placement with real-time stock validation, and an analytics dashboard powered by raw SQL aggregate queries.

## Live Demo
[Add your deployed link here once live]

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Products Page
![Products](screenshots/products.png)

### Orders Page
![Orders](screenshots/orders.png)

## Features

- **Product, Customer, and Category management** — full CRUD with proper error handling
- **Order placement with stock validation** — orders are rejected if requested quantity exceeds available stock; successful orders automatically decrement inventory
- **Analytics dashboard** — top-selling products, low-stock alerts, revenue by category, monthly revenue trend — all computed via raw SQL aggregate queries
- **Graceful constraint handling** — deleting a product/customer with existing orders returns a clear error instead of crashing; duplicate emails are caught and reported cleanly

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **Database:** MySQL
- **Frontend:** Jinja2 templates, vanilla JavaScript (fetch API), CSS
- **Server:** Uvicorn

## Database Schema
customers ──┐

            ├──< orders ──< order_items >── products ──> categories

users (auth, separate from customers)

Key design decisions:
- `order_items.unit_price` stores a **snapshot of the price at time of purchase**, so historical orders remain accurate even if a product's price changes later.
- Deletes on `products`/`customers` that would violate foreign key constraints (i.e., the record has order history) are caught and return a clean `400` error instead of a server crash.

## API Endpoints

| Resource | Endpoints |
|----------|-----------|
| Products | `GET /products/`, `GET /products/{id}`, `POST /products/`, `PUT /products/{id}`, `DELETE /products/{id}` |
| Customers | `GET /customers/`, `GET /customers/{id}`, `POST /customers/`, `PUT /customers/{id}`, `DELETE /customers/{id}` |
| Categories | `GET /categories/`, `POST /categories/`, `PUT /categories/{id}`, `DELETE /categories/{id}` |
| Orders | `GET /orders/`, `POST /orders/` (validates stock, decrements inventory) |
| Dashboard | `GET /dashboard/top-products`, `/low-stock`, `/revenue-by-category`, `/monthly-revenue`, `/customers-without-orders` |

Full interactive API docs available at `/docs` (Swagger UI).

## Setup & Run Locally

```bash
# Clone the repo
git clone <your-repo-url>
cd inventory-system

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up your .env file
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=orderManagement

# Run the schema (in MySQL)
# See schema.sql

# Start the server
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/` for the dashboard, or `http://127.0.0.1:8000/docs` for the API.

## Future Improvements

- Soft-delete pattern instead of hard deletes (preserve history while hiding discontinued products)
- Authentication for staff/admin actions
- Pagination for product/order lists
- Order status updates (pending → shipped → delivered)
