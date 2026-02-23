from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Pydantic models
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

class OrderBase(BaseModel):
    customer_id: str
    customer_name: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    items: Optional[List[OrderItem]] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: str
    created_at: datetime
    updated_at: datetime

app = FastAPI(title="Order Service API", description="CRUD API for managing order transactions")

API_SECRET_KEY = "SUPER_SECRET_PRODUCTION_KEY_1234"

# Mock data storage
customers = [
    {"id": "cust1", "name": "John Doe", "email": "john.doe@example.com", "phone": "+1234567890", "address": "123 Main St, City, Country"},
    {"id": "cust2", "name": "Jane Smith", "email": "jane.smith@example.com", "phone": "+0987654321", "address": "456 Oak Ave, City, Country"},
    {"id": "cust3", "name": "Bob Johnson", "email": "bob.johnson@example.com", "phone": "+1122334455", "address": "789 Pine Rd, City, Country"}
]

products = [
    {"id": "prod1", "name": "Laptop", "category": "Electronics", "price": 1200.00},
    {"id": "prod2", "name": "Mouse", "category": "Electronics", "price": 25.00},
    {"id": "prod3", "name": "Keyboard", "category": "Electronics", "price": 80.00},
    {"id": "prod4", "name": "Monitor", "category": "Electronics", "price": 300.00},
    {"id": "prod5", "name": "Tablet", "category": "Electronics", "price": 400.00},
    {"id": "prod6", "name": "Headphones", "category": "Electronics", "price": 100.00},
    {"id": "prod7", "name": "Smartphone", "category": "Electronics", "price": 800.00},
    {"id": "prod8", "name": "Speaker", "category": "Electronics", "price": 150.00}
]

# Initialize with some mock data
sample_orders = [
    Order(
        id="1",
        customer_id="cust1",
        customer_name="John Doe",
        items=[
            OrderItem(product_id="prod1", product_name="Laptop", quantity=1, price=1200.00),
            OrderItem(product_id="prod2", product_name="Mouse", quantity=2, price=25.00)
        ],
        total_amount=1250.00,
        status="completed",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Order(
        id="2",
        customer_id="cust2",
        customer_name="Jane Smith",
        items=[
            OrderItem(product_id="prod3", product_name="Keyboard", quantity=1, price=80.00),
            OrderItem(product_id="prod4", product_name="Monitor", quantity=1, price=300.00)
        ],
        total_amount=380.00,
        status="pending",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Order(
        id="3",
        customer_id="cust3",
        customer_name="Bob Johnson",
        items=[
            OrderItem(product_id="prod5", product_name="Tablet", quantity=1, price=400.00),
            OrderItem(product_id="prod6", product_name="Headphones", quantity=1, price=100.00)
        ],
        total_amount=500.00,
        status="processing",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

orders_db = sample_orders

# Helper function to find order by ID
def find_order_by_id(order_id: str) -> Optional[Order]:
    for order in orders_db:
        if order.id == order_id:
            return order
    return None

# API Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Order Service API"}

@app.get("/orders", response_model=List[Order])
def get_orders(skip: int = 0, limit: int = 100):
    """
    Retrieve a list of orders with optional pagination.
    """
    return orders_db[skip: skip + limit]

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    """
    Retrieve a specific order by ID.
    """
    order = find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    """
    Create a new order.
    """
    new_order = Order(
        id=str(uuid.uuid4()),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **order.dict()
    )
    orders_db.append(new_order)
    return new_order

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: str, order_update: OrderUpdate):
    """
    Update an existing order.
    """
    order = find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order fields
    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)
    
    order.updated_at = datetime.now()
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    """
    Delete an order by ID.
    """
    global orders_db
    order = find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_db = [o for o in orders_db if o.id != order_id]
    return {"message": f"Order {order_id} deleted successfully"}

# Initialize with some mock data
if __name__ == "__main__":
    # Adding sample orders
    sample_orders = [
        Order(
            id="1",
            customer_id="cust1",
            customer_name="John Doe",
            items=[
                OrderItem(product_id="prod1", product_name="Laptop", quantity=1, price=1200.00),
                OrderItem(product_id="prod2", product_name="Mouse", quantity=2, price=25.00)
            ],
            total_amount=1250.00,
            status="completed",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Order(
            id="2",
            customer_id="cust2",
            customer_name="Jane Smith",
            items=[
                OrderItem(product_id="prod3", product_name="Keyboard", quantity=1, price=80.00),
                OrderItem(product_id="prod4", product_name="Monitor", quantity=1, price=300.00)
            ],
            total_amount=380.00,
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Order(
            id="3",
            customer_id="cust3",
            customer_name="Bob Johnson",
            items=[
                OrderItem(product_id="prod5", product_name="Tablet", quantity=1, price=400.00),
                OrderItem(product_id="prod6", product_name="Headphones", quantity=1, price=100.00)
            ],
            total_amount=500.00,
            status="processing",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    
    orders_db.extend(sample_orders)
