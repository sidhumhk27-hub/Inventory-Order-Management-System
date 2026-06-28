from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    total_amount = 0
    order_items_to_create = []

    # Validate stock and calculate total BEFORE committing anything
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        total_amount += product.price * item.quantity
        order_items_to_create.append((product, item.quantity))

    new_order = models.Order(
        customer_id=order.customer_id,
        order_date=date.today(),
        status="pending",
        total_amount=total_amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product, qty in order_items_to_create:
        db.add(models.OrderItem(order_id=new_order.id, product_id=product.id,
                                 quantity=qty, unit_price=product.price))
        product.stock_quantity -= qty  # decrement stock

    db.commit()
    return new_order

@router.get("/", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()