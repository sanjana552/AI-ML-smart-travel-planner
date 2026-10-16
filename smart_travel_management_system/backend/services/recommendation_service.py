from datasets import load_dataset
from ml.trip_matcher import TripMatcher

DATASET_ID = "avihayamor/tripmatch-ai-dataset"
DATASET_CONFIG = "trip_plans"

_matcher = None

def get_matcher():
    global _matcher
    if _matcher is None:
        dataset = load_dataset(DATASET_ID, DATASET_CONFIG, split="train")
        frame = dataset.to_pandas()
        _matcher = TripMatcher(frame)
    return _matcher

def recommend_trips(destination, days, budget, companions, theme, pace):
    matcher = get_matcher()
    recommendations, notice = matcher.recommend(
        destination=destination,
        days=days,
        budget=budget,
        companions=companions,
        theme=theme,
        pace=pace,
        top_k=5,
    )
    return {"recommendations": recommendations, "notice": notice}
