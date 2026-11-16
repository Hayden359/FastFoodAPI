from flask import Flask, jsonify, request
import requests

from data import products

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the Fast Food API!"


@app.route("/inventory")
def get_products():

    category = request.args.get("category")

    if category:

        results = [
            product
            for product in products
            if product["category"].lower()
            == category.lower()
        ]

        return jsonify(results), 200

    return jsonify(products), 200


@app.route("/inventory/<int:product_id>")
def get_product(product_id):

    product = next(
        (
            p for p in products
            if p["id"] == product_id
        ),
        None
    )

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200


@app.route("/inventory", methods=["POST"])
def create_product():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    required = [
        "name",
        "category",
        "price"
    ]

    for field in required:

        if field not in data:

            return jsonify({
                "error":
                f"Missing field: {field}"
            }), 400

    new_product = {
        "id":
        max(
            [p["id"] for p in products],
            default=0
        ) + 1,

        "name":
        data["name"],

        "category":
        data["category"],

        "price":
        data["price"]
    }

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/inventory/<int:product_id>",
            methods=["PUT"])
def update_product(product_id):

    product = next(
        (
            p for p in products
            if p["id"] == product_id
        ),
        None
    )

    if not product:

        return jsonify({
            "error": "Product not found"
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    for key in (
        "name",
        "category",
        "price"
    ):

        if key in data:
            product[key] = data[key]

    return jsonify(product), 200


@app.route("/inventory/<int:product_id>",
            methods=["DELETE"])
def delete_product(product_id):

    product = next(
        (
            p for p in products
            if p["id"] == product_id
        ),
        None
    )

    if not product:

        return jsonify({
            "error": "Product not found"
        }), 404

    products.remove(product)

    return jsonify({
        "message":
        "Product deleted"
    }), 200


@app.route("/inventory/search")
def search_external_product():

    barcode = request.args.get(
        "barcode"
    )

    if not barcode:

        return jsonify({
            "error":
            "barcode required"
        }), 400

    try:

        response = requests.get(
            f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        )

        response.raise_for_status()

        data = response.json()

        product = data.get(
            "product",
            {}
        )

        return jsonify({
            "product_name":
            product.get(
                "product_name"
            ),

            "brands":
            product.get(
                "brands"
            ),

            "ingredients_text":
            product.get(
                "ingredients_text"
            ),

            "status":
            data.get(
                "status"
            )
        })

    except requests.RequestException:

        return jsonify({
            "error":
            "External API unavailable"
        }), 500


@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error":
        "Resource not found"
    }), 404


@app.route("/inventory/search/local")
def search_inventory():

    query = request.args.get("name")

    if not query:
        return jsonify({
            "error": "name required"
        }), 400

    results = [
        p
        for p in products
        if query.lower()
        in p["name"].lower()
    ]

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)