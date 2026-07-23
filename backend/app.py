import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, jsonify
from flask_cors import CORS

from emotion_module.predict import predict_emotion
from intent_module.intent_inference import predict_intent

from backend.models.model_loader import (
    load_person2_model
)

from backend.routes.chat_routes import create_chat_route
from context_module.memory import init_memory
init_memory()
app = Flask(__name__)

CORS(app)


print("Loading Person 1 model...")
person1_model = predict_emotion

print("Loading Person 2 model...")
person2_model = load_person2_model()


chat_route = create_chat_route(
    person1_model,
    person2_model,
    predict_intent
)

app.register_blueprint(chat_route)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "EmpathyAI Backend is running."
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )