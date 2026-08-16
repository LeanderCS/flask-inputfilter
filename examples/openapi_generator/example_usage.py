from flask import Flask, Response, g

from .filters import OrderInputFilter, ProductInputFilter, UserInputFilter

app = Flask(__name__)


@app.route("/api/users", methods=["POST"])
@UserInputFilter.validate()
def create_user():
    """
    Create a new user.

    Example request:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "active": true,
        "tags": ["developer", "python"],
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zipcode": "10001",
            "country": "USA"
        }
    }
    """
    return Response({"message": "User created", "data": g.validated_data}, 201)


@app.route("/api/products", methods=["POST"])
@ProductInputFilter.validate()
def create_product():
    """
    Create a new product.

    Example request:
    {
        "title": "Example Product",
        "description": "A great product",
        "price": 29.99,
        "status": "available",
        "category": {
            "id": 1,
            "name": "Electronics"
        },
        "images": [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ]
    }
    """
    return Response(
        {"message": "Product created", "data": g.validated_data}, 201
    )


@app.route("/api/orders", methods=["POST"])
@OrderInputFilter.validate()
def create_order():
    """
    Create a new order.

    Example request:
    {
        "user_id": 1,
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "price": 29.99
            }
        ],
        "order_date": "2024-01-15T10:30:00Z",
        "status": "pending"
    }
    """
    return Response(
        {"message": "Order created", "data": g.validated_data}, 201
    )


if __name__ == "__main__":
    app.run(debug=True)
