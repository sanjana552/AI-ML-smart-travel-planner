from pathlib import Path
from ml.trip_matcher import TripMatcher

_matcher = None


def get_matcher():
    """
    Initializes and returns a singleton instance of TripMatcher
    backed by the local Triip_HF_v4_10k.csv dataset.
    """
    global _matcher

    if _matcher is None:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "Triip_HF_v4_10k.csv"
        print(f"\nInitializing TripMatcher from local CSV: {csv_path}")

        _matcher = TripMatcher(csv_path)
        print("Travel recommendation service ready.")

    return _matcher


def recommend_trips(
    destination,
    days,
    budget=None,
    companions="Any",
    theme="Any",
    pace="Any"
):
    """
    Finds and ranks candidate itineraries from the local dataset.
    Returns a dictionary with recommendations list, notice, and source.
    """
    try:
        matcher = get_matcher()

        recommendations, notice = matcher.recommend(
            destination=destination,
            days=days,
            budget=budget,
            companions=companions,
            theme=theme,
            pace=pace,
            top_k=3
        )

        print(
            f"Dataset recommendations for '{destination}' ({days} days): "
            f"{len(recommendations)}"
        )

        return {
            "recommendations": recommendations,
            "notice": notice,
            "source": "Dataset Recommendation" if recommendations else "none"
        }

    except Exception as error:
        print("DATASET RECOMMENDATION ERROR:", repr(error))
        raise
