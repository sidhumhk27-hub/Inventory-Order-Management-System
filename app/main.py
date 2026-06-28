from fastapi import FastAPI , Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import products, customers, categories, orders, dashboard

Base.metadata.create_all(bind=engine)  # creates tables if not exist (safe since they already exist)

app = FastAPI(title="Inventory & Order Management System")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(dashboard.router)

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")

@app.get("/products-page")
def products_page(request: Request):
    return templates.TemplateResponse(request, "products.html")

@app.get("/orders-page")
def orders_page(request: Request):
    return templates.TemplateResponse(request, "orders.html")

@app.get("/customers-page")
def customers_page(request: Request):
    return templates.TemplateResponse(request, "customers.html")