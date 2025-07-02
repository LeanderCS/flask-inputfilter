from flask import Flask, Response, g

from .filters import ProductInputFilter, ProfileInputFilter, UserInputFilter

app = Flask(__name__)


@app.route("/api/user", methods=["POST"], endpoint="create-user")
@UserInputFilter.validate()
def create_user():
    return Response(
        {"message": "User created successfully", "data": g.validated_data},
        201,
    )


@app.route("/api/profile", methods=["POST"], endpoint="create-profile")
@ProfileInputFilter.validate()
def create_profile():
    return Response(
        {
            "message": "Profile created successfully",
            "data": g.validated_data,
        },
        201,
    )


@app.route("/api/product", methods=["POST"], endpoint="create-product")
@ProductInputFilter.validate()
def create_products():
    return Response(
        {
            "message": "Products created successfully",
            "data": g.validated_data,
        },
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
