# app/routes.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from .emotion_detector import detect_emotion_from_base64
from .recommender import get_movies_for_emotion

app = Flask(__name__)
CORS(app)

@app.route("/detect", methods=["POST"])
def detect_and_recommend():
    """
    Expects JSON: { "image": "<base64_string>" }
    Returns: { "emotion": "...", "confidence": 0.95, "recommendations": [...] }
    """
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    # Step 1: Detect emotion
    emotion, confidence = detect_emotion_from_base64(data["image"])
    if not emotion:
        return jsonify({"error": "Emotion detection failed"}), 500

    # Step 2: Get recommendations
    recommendations = get_movies_for_emotion(emotion, num_results=5)

    return jsonify({
        "emotion": emotion,
        "confidence": confidence,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
