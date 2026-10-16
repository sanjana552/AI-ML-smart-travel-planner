from flask import Flask, jsonify
from flask_cors import CORS
from routes.travel_routes import travel_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(travel_bp, url_prefix="/api")

@app.get("/")
def home():
    return jsonify({
        "message": "Smart Travel Planner API is running",
        "endpoint": "POST /api/itinerary"
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
