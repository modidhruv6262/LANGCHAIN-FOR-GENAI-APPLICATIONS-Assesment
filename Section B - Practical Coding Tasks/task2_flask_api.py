import numpy as np
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

candidate_paths = [
    "delivery_model.joblib",
    "Section B - Practical Coding Tasks/delivery_model.joblib",
    "../delivery_model.joblib"
]

model = None
for path in candidate_paths:
    try:
        model = joblib.load(path)
        break
    except Exception:
        continue

if model is None:
    raise RuntimeError("Could not load delivery_model.joblib from candidate paths.")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be a valid JSON object"}), 400

    required_fields = ["distance_km", "num_items", "rain_flag"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    try:
        distance = float(data["distance_km"])
        items = int(data["num_items"])
        rain = int(data["rain_flag"])
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid field types: {str(e)}"}), 400

    features = np.array([[distance, items, rain]])
    prediction = float(model.predict(features)[0])
    rounded_prediction = round(prediction, 1)

    return jsonify({
        "status": "success",
        "predicted_delivery_time_min": rounded_prediction
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
