from flask import Flask, request, jsonify

app = Flask(__name__)

# dummy account with a starting balance
account = {
    "id": 123,
    "balance": 1000
}


def deduct_from_balance(amount):
    if account["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    account["balance"] -= amount
    return jsonify({"message": f"Successfully deducted {amount}"}), 200


@app.route('/api/deduct', methods=['POST'])
def deduct():

    data = request.get_json()

    if not data.get("amount"):
        return jsonify({"error": "No amount specified"}), 400

    return deduct_from_balance(data["amount"])


if __name__ == '__main__':
    app.run(debug=True)
