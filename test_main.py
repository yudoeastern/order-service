import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

def test_read_root():
    """Test the root endpoint"""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Order Service API"}

def test_get_orders():
    """Test getting all orders"""
    with TestClient(app) as client:
        response = client.get("/orders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 0  # Should have at least the sample orders
    
def test_create_order():
    """Test creating a new order"""
    new_order_data = {
        "customer_id": "cust4",
        "customer_name": "Alice Wilson",
        "items": [
            {
                "product_id": "prod7",
                "product_name": "Smartphone",
                "quantity": 1,
                "price": 800.00
            }
        ],
        "total_amount": 800.00,
        "status": "pending"
    }
    
    with TestClient(app) as client:
        response = client.post("/orders", json=new_order_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_id"] == "cust4"
        assert data["customer_name"] == "Alice Wilson"
        assert data["total_amount"] == 800.00
        assert data["status"] == "pending"
        assert "id" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["product_name"] == "Smartphone"
    
def test_get_specific_order():
    """Test getting a specific order by ID"""
    with TestClient(app) as client:
        # First create an order to retrieve
        new_order_data = {
            "customer_id": "cust5",
            "customer_name": "Test Customer",
            "items": [
                {
                    "product_id": "prod8",
                    "product_name": "Speaker",
                    "quantity": 2,
                    "price": 150.00
                }
            ],
            "total_amount": 300.00,
            "status": "processing"
        }
        
        create_response = client.post("/orders", json=new_order_data)
        assert create_response.status_code == 200
        order_id = create_response.json()["id"]
        
        # Now retrieve the created order
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == order_id
        assert data["customer_id"] == "cust5"
        assert data["customer_name"] == "Test Customer"
        assert data["total_amount"] == 300.00
