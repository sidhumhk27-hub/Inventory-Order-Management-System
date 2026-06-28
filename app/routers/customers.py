from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=list[schemas.CustomerOut])
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

from sqlalchemy.exc import IntegrityError

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerBase, db: Session = Depends(get_db)):
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A customer with this email already exists."
        )
    db.refresh(new_customer)
    return new_customer

@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, updated: schemas.CustomerBase, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in updated.dict().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

from sqlalchemy.exc import IntegrityError

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    try:
        db.delete(customer)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete this customer — they have existing orders."
        )
    return {"message": "Customer deleted"}