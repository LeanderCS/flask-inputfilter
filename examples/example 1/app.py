from flask import Flask, jsonify, g
from .filters import UserInputFilter, ProfileInputFilter, ProductInputFilter

app = Flask(__name__)

@app.route('/api/user', methods=['POST'], endpoint='create-user')
@UserInputFilter.validate()
def create_user():
    return jsonify({"message": "User created successfully", "data": g.validated_data}), 201

@app.route('/api/profile', methods=['POST'], endpoint='create-profile')
@ProfileInputFilter.validate()
def create_profile():
    return jsonify({"message": "Profile created successfully", "data": g.validated_data}), 201

@app.route('/api/product', methods=['POST'], endpoint='create-product')
@ProductInputFilter.validate()
def create_products():
    return jsonify({"message": "Products created successfully", "data": g.validated_data}), 201

if __name__ == '__main__':
    app.run(debug=True)
