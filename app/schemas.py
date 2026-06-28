from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class CategoryOut(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    stock_quantity: int

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemBase]

class OrderOut(BaseModel):
    id: int
    customer_id: int
    order_date: date
    status: str
    total_amount: float
    class Config:
        from_attributes = True