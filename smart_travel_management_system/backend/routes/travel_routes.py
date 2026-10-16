from flask import Blueprint, jsonify, request
from services.recommendation_service import recommend_trips

travel_bp = Blueprint("travel", __name__)

@travel_bp.post("/itinerary")
def itinerary():
    payload = request.get_json(silent=True) or {}
    destination = str(payload.get("destination", "")).strip()
    if not destination:
        return jsonify({"error": "Please enter a destination."}), 400

    try:
        result = recommend_trips(
            destination=destination,
            days=int(payload.get("days", 3)),
            budget=str(payload.get("budget", "Any")),
            companions=str(payload.get("companions", "Any")),
            theme=str(payload.get("theme", "Any")),
            pace=str(payload.get("pace", "Any")),
        )
        return jsonify(result)
    except Exception as exc:
        return jsonify({
            "error": "Recommendation service failed. Check the terminal for the backend error.",
            "details": str(exc)
        }), 500
