import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from ml.curated_attractions import get_attractions_for_destination

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from backend/.env")
    return Groq(api_key=api_key)


def infer_num_travellers(companions):
    comp = str(companions or "").strip().lower()
    if "solo" in comp:
        return 1
    elif "couple" in comp:
        return 2
    elif "family" in comp:
        return 4
    elif "friend" in comp:
        return 3
    return 2


def heuristic_budget_estimate(destination, days, user_budget, companions, budget_tier="mid-range"):
    """
    Fallback deterministic cost estimate in INR if the Groq service
    is unreachable, ensuring uninterrupted system availability.
    """
    num_travellers = infer_num_travellers(companions)
    days = max(1, int(days))
    tier = str(budget_tier or "mid-range").lower()

    if "lux" in tier:
        hotel_per_room = 6000
        food_per_person = 1500
        transit_per_day = 1800
        sightseeing_per_day = 1200
    elif "budg" in tier:
        hotel_per_room = 1200
        food_per_person = 450
        transit_per_day = 500
        sightseeing_per_day = 300
    else:  # mid-range
        hotel_per_room = 2500
        food_per_person = 800
        transit_per_day = 900
        sightseeing_per_day = 600

    rooms = max(1, (num_travellers + 1) // 2)
    accommodation = hotel_per_room * rooms * days
    food = food_per_person * num_travellers * days
    local_transport = transit_per_day * days
    attraction_fees = sightseeing_per_day * days
    miscellaneous = int((accommodation + food + local_transport + attraction_fees) * 0.1)

    estimated_total = accommodation + food + local_transport + attraction_fees + miscellaneous
    per_person = round(estimated_total / num_travellers)

    user_b = float(user_budget) if user_budget else float(estimated_total)
    diff_pct = (user_b - estimated_total) / estimated_total

    if diff_pct >= -0.15:
        status = "Within budget"
        is_realistic = True
        explanation = f"Estimated trip cost (₹{estimated_total:,}) is well aligned with your target budget of ₹{int(user_b):,}."
    elif diff_pct >= -0.40:
        status = "Budget is tight"
        is_realistic = True
        explanation = f"Your target budget of ₹{int(user_b):,} is somewhat tight compared to the estimated ₹{estimated_total:,}. Consider opting for budget homestays or shared transport."
    else:
        status = "Unrealistic budget"
        is_realistic = False
        explanation = f"Your target budget of ₹{int(user_b):,} is significantly below the minimum viable estimated cost of ₹{estimated_total:,} for {days} days in {destination}."

    return {
        "accommodation": accommodation,
        "food": food,
        "local_transport": local_transport,
        "attraction_fees": attraction_fees,
        "miscellaneous": miscellaneous,
        "estimated_total": estimated_total,
        "per_person_cost": per_person,
        "num_travellers": num_travellers,
        "user_budget": int(user_b),
        "budget_status": status,
        "is_realistic": is_realistic,
        "assumptions": f"Estimated for {num_travellers} traveller(s) based on {tier} standards in {destination} for {days} days.",
        "budget_explanation": explanation,
        "disclaimer": "AI/heuristic estimate in INR. Live prices vary by season, availability, and specific bookings."
    }


def local_attraction_itinerary_fallback(destination, days, budget, companions, theme, pace, budget_tier="mid-range"):
    """
    Constructs a specific, multi-day itinerary using verified local attractions
    if the AI service is unreachable, preventing generic placeholder text.
    """
    known_attractions = get_attractions_for_destination(destination)
    if not known_attractions:
        known_attractions = [
            f"Historic Center of {destination}",
            f"{destination} Heritage Palace / Monument",
            f"Central Lake & Promenade in {destination}",
            f"Famous Cultural Museum of {destination}",
            f"Iconic Temple / Cathedral in {destination}",
            f"Traditional Crafts Bazaar in {destination}",
            f"Scenic Viewpoint of {destination}",
            f"Botanical Gardens of {destination}"
        ]

    daily_plan = []
    attraction_idx = 0
    total_places = len(known_attractions)

    times = [
        ("Morning", "09:00 AM", "Morning exploration and sightseeing"),
        ("Afternoon", "01:30 PM", "Afternoon visit, cultural tour and local lunch"),
        ("Evening", "06:00 PM", "Evening stroll, sunset viewing and local dining")
    ]

    for day_num in range(1, days + 1):
        stops = []
        for period, t_val, act_tmpl in times:
            place_name = known_attractions[attraction_idx % total_places]
            attraction_idx += 1
            stops.append({
                "period": period,
                "time": t_val,
                "place": place_name,
                "activity": f"{act_tmpl} at {place_name}; experience local {theme} culture.",
                "travel_duration": "20-30 mins"
            })

        daily_plan.append({
            "day": day_num,
            "title": f"Day {day_num}: Exploring {stops[0]['place']} & Landmarks",
            "stops": stops,
            "estimated_day_cost": None
        })

    budget_breakdown = heuristic_budget_estimate(destination, days, budget, companions, budget_tier)

    return {
        "destination": destination,
        "duration_days": days,
        "days": days,
        "budget_amount": float(budget),
        "companions": companions,
        "theme": theme,
        "pace": pace,
        "daily_plan": daily_plan,
        "budget_breakdown": budget_breakdown,
        "trip_plan": f"A comprehensive {days}-day itinerary exploring authentic sights across {destination}.",
        "source": "Dataset Recommendation (AI-Enriched)",
        "notice": f"Curated itinerary from Triip travel dataset for {destination}, verified with destination landmarks."
    }


def enrich_dataset_itinerary(
    destination,
    days,
    budget,
    dataset_plan,
    companions="Any",
    theme="Any",
    pace="Any"
):
    """
    Enriches a dataset recommendation by replacing generic activity placeholders
    with REAL, FAMOUS, and VERIFIED attractions in the destination, extending the plan
    to cover all requested days, and estimating an INR budget breakdown.
    """
    known_attractions = get_attractions_for_destination(destination)
    attraction_hint = ""
    if known_attractions:
        attraction_hint = f"Verified major landmarks in {destination}: {', '.join(known_attractions[:12])}."

    num_trav = infer_num_travellers(companions)
    budget_tier = dataset_plan.get("budget_tier", "mid-range")
    dataset_theme = dataset_plan.get("theme", "sightseeing")
    raw_itinerary = str(dataset_plan.get("raw_itinerary", ""))

    prompt = f"""
You are an expert travel planner for Indian tourism.
A travel dataset matched the following trip framework for {destination}, but its activities contain generic placeholders.
Your job is to ENRICH this itinerary with REAL, FAMOUS, SPECIFIC tourist attractions in {destination} and an accurate INR budget estimation.

TRIP DETAILS:
- Destination: {destination} (MUST strictly be {destination}. Never change city!)
- Duration: EXACTLY {days} days (You MUST produce exactly {days} day objects in daily_plan)
- Target Budget: INR {budget}
- Travelling with: {companions} (approx {num_trav} traveller(s))
- Theme: {theme} (Dataset theme context: {dataset_theme})
- Preferred Pace: {pace}
- Budget Tier: {budget_tier}
{attraction_hint}

RAW DATASET FRAMEWORK:
{raw_itinerary[:500]}

REQUIREMENTS:
1. Generate an itinerary for EXACTLY {days} days. Every day must be clearly numbered and titled.
2. For each day, create 2 to 3 stops (Morning, Afternoon, Evening).
3. In each stop:
   - `place`: Name of a REAL, RECOGNIZABLE, famous attraction, landmark, temple, beach, fort or historic spot in {destination} (e.g. for Delhi: Red Fort, Qutub Minar, Humayun's Tomb, India Gate, Lotus Temple, Jama Masjid, Akshardham; for Jaipur: Amber Fort, Hawa Mahal, City Palace, Jantar Mantar, Nahargarh Fort; for Goa: Baga Beach, Fort Aguada, Basilica of Bom Jesus, Dudhsagar Falls, Chapora Fort; for Manali: Hadimba Temple, Solang Valley, Rohtang Pass, Vashisht Springs).
   - NEVER use generic placeholders like "indoor attractions", "lunch experience", "garden walks", "free attractions", or "open-air markets". Name the actual attraction!
   - `time`: Recommended visiting time (e.g. "09:00 AM", "01:30 PM", "06:30 PM").
   - `period`: "Morning", "Afternoon", or "Evening".
   - `activity`: Clear, practical activity description with cultural, scenic, or historical insights.
   - `travel_duration`: Realistic travel time or walking distance (e.g. "20 mins by auto/cab", "Walking distance").
4. Practical routing: Group geographically close attractions together on the same day to minimize transit.
5. Provide a realistic budget estimation in Indian Rupees (INR):
   - `accommodation`: Hotel/homestay cost suitable for {num_trav} travellers for {days} days in {budget_tier} tier.
   - `food`: Meal expenses for all travellers over {days} days.
   - `local_transport`: Autos, cabs, or rentals in {destination}.
   - `attraction_fees`: Monument entry tickets and activity fees.
   - `miscellaneous`: Buffer, water, snacks, tips.
   - `estimated_total`: Exact sum of above 5 categories.
   - `per_person_cost`: Round(estimated_total / {num_trav}).
   - `budget_status`: "Within budget", "Budget is tight", or "Unrealistic budget".
   - `is_realistic`: Boolean.
   - `assumptions`: Clear explanation of assumed lodging, food, and transport standards.
   - `budget_explanation`: Advice on whether the user's budget fits.
6. Return strictly valid JSON only.

JSON FORMAT:
{{
  "destination": "{destination}",
  "duration_days": {days},
  "budget_breakdown": {{
    "accommodation": 5000,
    "food": 3600,
    "local_transport": 1800,
    "attraction_fees": 1200,
    "miscellaneous": 1000,
    "estimated_total": 12600,
    "per_person_cost": 6300,
    "num_travellers": {num_trav},
    "user_budget": {budget},
    "budget_status": "Within budget",
    "is_realistic": true,
    "assumptions": "Assumed {num_trav} traveller(s) staying in {budget_tier} lodging with local dining in {destination}.",
    "budget_explanation": "Detailed explanation of budget feasibility.",
    "disclaimer": "AI-generated cost estimate in INR. Live prices vary by season and booking time."
  }},
  "daily_plan": [
    {{
      "day": 1,
      "title": "Day 1: <Theme / District in {destination}>",
      "stops": [
        {{
          "period": "Morning",
          "time": "09:00 AM",
          "place": "<Real Attraction Name>",
          "activity": "<Specific activity and highlight>",
          "travel_duration": "20 mins"
        }}
      ]
    }}
  ],
  "trip_plan": "A concise summary highlighting the real attractions across all {days} days in {destination}."
}}
"""

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a master travel planner for {destination}. "
                        "You always recommend real, specific attractions and never generic placeholders. "
                        "Return strictly valid JSON only."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
            max_completion_tokens=5000
        )

        content = response.choices[0].message.content
        enriched = json.loads(content)

        daily_plan = enriched.get("daily_plan", [])
        if not isinstance(daily_plan, list) or len(daily_plan) == 0:
            raise ValueError("Enriched daily_plan is missing or empty.")

        # Ensure numeric fields on budget_breakdown
        bb = enriched.get("budget_breakdown", {})
        acc = int(bb.get("accommodation", 0))
        fd = int(bb.get("food", 0))
        tr = int(bb.get("local_transport", 0))
        at = int(bb.get("attraction_fees", 0))
        ms = int(bb.get("miscellaneous", 0))
        tot = acc + fd + tr + at + ms
        bb["accommodation"] = acc
        bb["food"] = fd
        bb["local_transport"] = tr
        bb["attraction_fees"] = at
        bb["miscellaneous"] = ms
        bb["estimated_total"] = tot
        bb["num_travellers"] = int(bb.get("num_travellers", num_trav))
        bb["per_person_cost"] = int(
            bb.get("per_person_cost", round(tot / max(1, bb["num_travellers"])))
        )
        bb["user_budget"] = float(budget)
        if not bb.get("disclaimer"):
            bb["disclaimer"] = "AI-generated cost estimate in INR. Live prices vary by season and booking time."

        enriched["destination"] = destination
        enriched["duration_days"] = int(days)
        enriched["days"] = int(days)
        enriched["budget_amount"] = float(budget)
        enriched["companions"] = companions
        enriched["theme"] = theme
        enriched["pace"] = pace
        enriched["budget_tier"] = budget_tier
        enriched["match_score"] = dataset_plan.get("match_score")
        enriched["source"] = "Dataset Recommendation (AI-Enriched)"
        enriched["notice"] = (
            f"Curated itinerary framework from Triip travel dataset for {destination}, "
            "enriched with verified local attractions via Groq AI."
        )

        return enriched

    except Exception as exc:
        print(f"Warning: Groq AI itinerary enrichment encountered an issue ({exc}). Using curated attraction fallback.")
        fallback = local_attraction_itinerary_fallback(
            destination, days, budget, companions, theme, pace, budget_tier
        )
        fallback["match_score"] = dataset_plan.get("match_score")
        return fallback


def generate_ai_itinerary(
    destination,
    days,
    budget,
    companions="Any",
    theme="Any",
    pace="Any"
):
    """
    Generates a full travel itinerary using Groq AI when no dataset match is found
    (e.g., international destinations like Paris, Zurich, or unlisted cities).
    Includes real, specific attractions and structured budget breakdown in INR.
    """
    client = get_groq_client()
    num_trav = infer_num_travellers(companions)

    prompt = f"""
Create a comprehensive, day-by-day travel itinerary for {destination}.

USER INPUT:
Destination: {destination} (MUST strictly be {destination}. Do not substitute another city!)
Duration: EXACTLY {days} days
Total budget: INR {budget}
Travelling with: {companions} (approx {num_trav} traveller(s))
Main interest: {theme}
Travel pace: {pace}

RULES:
- Destination must be strictly: {destination}.
- Use authentic, well-known attractions believed to exist in {destination} (e.g. for Paris: Eiffel Tower, Louvre Museum, Notre-Dame, Montmartre, Arc de Triomphe).
- Format daily_plan as a list of exactly {days} days.
- Each day must have 2 to 3 stops: Morning (e.g. 09:00 AM), Afternoon (e.g. 01:30 PM), and Evening (e.g. 06:30 PM).
- For each stop, provide a specific place name, time, period, and clear activity description.
- Provide a structured budget breakdown in Indian Rupees (INR) with estimated_total and per_person_cost.
- State whether the requested budget of INR {budget} is realistic.
- Return valid JSON only, no markdown fencing, no additional prose.

RETURN THIS EXACT JSON STRUCTURE:
{{
  "destination": "{destination}",
  "duration_days": {days},
  "budget_amount": {budget},
  "companions": "{companions}",
  "pace": "{pace}",
  "theme": "{theme}",
  "source": "Generative AI",
  "notice": "AI-generated itinerary via Groq. Verify prices, opening hours and arrangements before travelling.",
  "budget_breakdown": {{
    "accommodation": 0,
    "food": 0,
    "local_transport": 0,
    "attraction_fees": 0,
    "miscellaneous": 0,
    "estimated_total": 0,
    "per_person_cost": 0,
    "num_travellers": {num_trav},
    "user_budget": {budget},
    "budget_status": "Within budget",
    "is_realistic": true,
    "assumptions": "Summary of budget assumptions in {destination} for {days} days.",
    "budget_explanation": "Explanation of budget fit and suggestions.",
    "disclaimer": "AI-generated estimate in INR. Not verified live prices."
  }},
  "daily_plan": [
    {{
      "day": 1,
      "title": "Day 1: Arrival & Iconic Landmarks",
      "stops": [
        {{
          "period": "Morning",
          "time": "09:00 AM",
          "place": "<Real Attraction Name>",
          "activity": "<Specific activity and description>",
          "travel_duration": "30 mins"
        }}
      ]
    }}
  ],
  "trip_plan": "A concise overview of the {days}-day journey in {destination}."
}}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a careful travel-planning assistant for {destination}. "
                    "You always recommend real, specific attractions and never generic placeholders. "
                    "Return valid JSON only."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
        max_completion_tokens=5000
    )

    content = response.choices[0].message.content

    try:
        itinerary = json.loads(content)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Groq returned an invalid JSON itinerary.") from exc

    daily_plan = itinerary.get("daily_plan")
    if not isinstance(daily_plan, list) or not daily_plan:
        raise RuntimeError("AI did not return a valid daily itinerary.")

    itinerary["destination"] = destination
    itinerary["duration_days"] = int(days)
    itinerary["days"] = int(days)
    itinerary["budget_amount"] = float(budget)
    itinerary["companions"] = companions
    itinerary["theme"] = theme
    itinerary["pace"] = pace
    itinerary["source"] = "Generative AI"
    itinerary["match_score"] = None
    itinerary.setdefault(
        "notice",
        "AI-generated itinerary via Groq. Verify prices, opening hours and arrangements before travelling."
    )

    # Sanitize budget breakdown
    breakdown = itinerary.get("budget_breakdown")
    if not isinstance(breakdown, dict):
        itinerary["budget_breakdown"] = heuristic_budget_estimate(
            destination, days, budget, companions
        )
    else:
        acc = int(breakdown.get("accommodation", 0))
        fd = int(breakdown.get("food", 0))
        tr = int(breakdown.get("local_transport", 0))
        at = int(breakdown.get("attraction_fees", 0))
        ms = int(breakdown.get("miscellaneous", 0))
        tot = acc + fd + tr + at + ms
        breakdown["accommodation"] = acc
        breakdown["food"] = fd
        breakdown["local_transport"] = tr
        breakdown["attraction_fees"] = at
        breakdown["miscellaneous"] = ms
        breakdown["estimated_total"] = tot
        breakdown["num_travellers"] = int(breakdown.get("num_travellers", num_trav))
        breakdown["per_person_cost"] = int(
            breakdown.get("per_person_cost", round(tot / max(1, breakdown["num_travellers"])))
        )
        breakdown["user_budget"] = float(budget)
        if not breakdown.get("disclaimer"):
            breakdown["disclaimer"] = "AI-generated estimate in INR. Not verified live prices."

    return itinerary


def estimate_trip_budget(
    destination,
    days,
    user_budget,
    companions="Any",
    theme="Any",
    pace="Any",
    budget_tier="mid-range",
    itinerary_context=""
):
    """
    Standalone budget estimation function if needed independently.
    """
    try:
        client = get_groq_client()
        num_trav = infer_num_travellers(companions)

        prompt = f"""
Estimate a realistic travel budget in Indian Rupees (INR) for this trip.

TRIP DETAILS:
- Destination: {destination}
- Duration: {days} days
- User Target Budget: INR {user_budget}
- Travelling with: {companions} (approx {num_trav} traveller(s))
- Travel theme / style: {theme}
- Pace: {pace}
- Target tier: {budget_tier}

RULES:
1. Provide realistic cost estimates in Indian Rupees (INR) for:
   - accommodation
   - food
   - local_transport
   - attraction_fees
   - miscellaneous
2. estimated_total MUST equal sum of above 5.
3. Compute per_person_cost = round(estimated_total / {num_trav}).
4. Evaluate user budget realism (Within budget, Budget is tight, or Unrealistic budget).
5. Return strictly valid JSON only.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional travel cost estimator for India. Return strictly valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
            max_completion_tokens=1500
        )

        content = response.choices[0].message.content
        budget_data = json.loads(content)

        accommodation = int(budget_data.get("accommodation", 0))
        food = int(budget_data.get("food", 0))
        transport = int(budget_data.get("local_transport", 0))
        attraction = int(budget_data.get("attraction_fees", 0))
        misc = int(budget_data.get("miscellaneous", 0))
        total = accommodation + food + transport + attraction + misc

        budget_data["accommodation"] = accommodation
        budget_data["food"] = food
        budget_data["local_transport"] = transport
        budget_data["attraction_fees"] = attraction
        budget_data["miscellaneous"] = misc
        budget_data["estimated_total"] = total
        budget_data["num_travellers"] = int(budget_data.get("num_travellers", num_trav))
        budget_data["per_person_cost"] = int(
            budget_data.get("per_person_cost", round(total / max(1, budget_data["num_travellers"])))
        )
        budget_data["user_budget"] = float(user_budget) if user_budget else float(total)

        return budget_data

    except Exception as exc:
        print(f"Warning: Groq AI budget estimation error ({exc}). Using heuristic estimator.")
        return heuristic_budget_estimate(destination, days, user_budget, companions, budget_tier)
