# Order Service API

This is a FastAPI-based service for managing order transactions. It provides CRUD operations for orders using mock data for demonstration purposes.

## Features

- Create new orders
- Read existing orders
- Update order information
- Delete orders
- List all orders with pagination support

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv-cs
   ```

2. Activate the virtual environment:
   ```bash
   source venv-cs/bin/activate  # On Windows: venv-cs\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /orders` - Get all orders (with optional pagination)
- `GET /orders/{order_id}` - Get a specific order
- `POST /orders` - Create a new order
- `PUT /orders/{order_id}` - Update an existing order
- `DELETE /orders/{order_id}` - Delete an order

## License

This project is licensed under the MIT License.# test
trigger
# trigger
