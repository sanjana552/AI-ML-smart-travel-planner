from flask import Blueprint, jsonify, request
from services.recommendation_service import recommend_trips
from services.ai_itinerary_service import generate_ai_itinerary, enrich_dataset_itinerary

travel_bp = Blueprint("travel", __name__)


@travel_bp.post("/itinerary")
def itinerary():
    payload = request.get_json(silent=True) or {}

    destination = str(payload.get("destination", "")).strip()
    companions = str(payload.get("companions", "Any")).strip()
    theme = str(payload.get("theme", "Any")).strip()
    pace = str(payload.get("pace", "Any")).strip()

    if not destination:
        return jsonify({"error": "Please enter a destination."}), 400

    try:
        days = int(payload.get("days", 0))
        budget = float(payload.get("budget", 0))
    except (TypeError, ValueError):
        return jsonify({
            "error": "Days must be a whole number and budget must be numeric."
        }), 400

    if days < 1 or days > 30:
        return jsonify({
            "error": "Trip duration must be between 1 and 30 days."
        }), 400

    if budget <= 0:
        return jsonify({
            "error": "Budget must be greater than zero."
        }), 400

    # 1. Search local dataset first
    try:
        result = recommend_trips(
            destination=destination,
            days=days,
            budget=budget,
            companions=companions,
            theme=theme,
            pace=pace
        )

        recs = result.get("recommendations", [])

        if recs:
            top_plan = recs[0]

            # Enrich dataset plan with specific, verified local attractions and exact duration
            enriched_plan = enrich_dataset_itinerary(
                destination=top_plan.get("destination", destination),
                days=days,
                budget=budget,
                dataset_plan=top_plan,
                companions=companions,
                theme=theme,
                pace=pace
            )

            print(
                f"Returning enriched Dataset Recommendation for '{destination}' "
                f"({days} days, score: {enriched_plan.get('match_score')})."
            )

            return jsonify({
                "recommendations": [enriched_plan],
                "notice": enriched_plan.get("notice"),
                "source": enriched_plan.get("source", "Dataset Recommendation (AI-Enriched)")
            })

        print(f"No suitable dataset match for '{destination}' ({days} days). Falling back to Groq Generative AI.")

    except Exception as exc:
        print("DATASET PIPELINE ERROR:", repr(exc))
        print("Falling back to Groq Generative AI.")

    # 2. Fall back to Generative AI if no dataset match exists (e.g. Paris, international destinations)
    try:
        ai_plan = generate_ai_itinerary(
            destination=destination,
            days=days,
            budget=budget,
            companions=companions,
            theme=theme,
            pace=pace
        )

        ai_plan["source"] = "Generative AI"

        notice = ai_plan.get(
            "notice",
            "AI-generated itinerary via Groq. Verify prices, opening hours and arrangements before travelling."
        )

        print(f"Returning Generative AI itinerary for '{destination}' ({days} days).")

        return jsonify({
            "recommendations": [ai_plan],
            "notice": notice,
            "source": "Generative AI"
        })

    except Exception as exc:
        print("AI ITINERARY GENERATION ERROR:", repr(exc))

        return jsonify({
            "error": "Could not generate travel itinerary.",
            "details": str(exc)
        }), 502
