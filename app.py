from flask import Flask, request, jsonify
from nearest_partner import load_partners, find_nearest_eligible

app = Flask(__name__)
partners = load_partners()


@app.after_request
def add_cors_headers(response):
    # allows the React frontend (running on a different port) to call this API
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/nearest-partner", methods=["POST"])
def nearest_partner():
    data = request.get_json()

    # basic input validation - if something's missing, say so instead of crashing
    required = ["lat", "lng", "loan_category"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    results = find_nearest_eligible(
        user_lat=data["lat"],
        user_lng=data["lng"],
        loan_category=data["loan_category"],
        partners=partners,
    )

    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
