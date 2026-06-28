from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    query = text("""
        SELECT p.name, SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY oi.product_id, p.name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

@router.get("/low-stock")
def low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    query = text("""
        SELECT id, name, stock_quantity
        FROM products
        WHERE stock_quantity < :threshold
    """)
    result = db.execute(query, {"threshold": threshold})
    return [dict(row._mapping) for row in result]

@router.get("/revenue-by-category")
def revenue_by_category(db: Session = Depends(get_db)):
    query = text("""
        SELECT c.name AS category, SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY total_revenue DESC
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

@router.get("/monthly-revenue")
def monthly_revenue(db: Session = Depends(get_db)):
    query = text("""
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
        FROM orders
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY month
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

@router.get("/customers-without-orders")
def customers_without_orders(db: Session = Depends(get_db)):
    query = text("""
        SELECT c.id, c.name, c.email
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        WHERE o.id IS NULL
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]