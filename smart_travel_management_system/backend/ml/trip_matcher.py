import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_ID = "avihayamor/tripmatch-ai-embedding-model"

class TripMatcher:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame.copy()
        for col in self.frame.columns:
            if self.frame[col].dtype == "object":
                self.frame[col] = self.frame[col].fillna("").astype(str)
        self.model = SentenceTransformer(MODEL_ID)
        self.text_col = "embedding_text" if "embedding_text" in self.frame.columns else "trip_plan"
        if self.text_col not in self.frame.columns:
            raise ValueError("Dataset has neither 'embedding_text' nor 'trip_plan' column.")
        texts = self.frame[self.text_col].fillna("").astype(str).tolist()
        self.embeddings = self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=True, batch_size=64
        )

    def _filter_if_available(self, frame, column, value):
        if value == "Any" or column not in frame.columns:
            return frame
        mask = frame[column].astype(str).str.contains(value, case=False, regex=False, na=False)
        # Keep current candidates if exact structured filtering would remove every row.
        return frame[mask] if mask.any() else frame

    def recommend(self, destination, days, budget, companions, theme, pace, top_k=5):
        original = self.frame
        candidates = original.copy()
        notices = []

        if "destination" in candidates.columns:
            mask = candidates["destination"].str.contains(destination, case=False, regex=False, na=False)
            if mask.any():
                candidates = candidates[mask]
            else:
                notices.append(
                    f"No exact destination match for '{destination}' was found. Showing closest available dataset alternatives."
                )

        if "duration_days" in candidates.columns:
            exact = candidates[candidates["duration_days"].astype(str).eq(str(days))]
            if not exact.empty:
                candidates = exact
            else:
                notices.append("No exact duration match was available; closest matching trip plans may have a different duration.")

        candidates = self._filter_if_available(candidates, "budget", budget)
        candidates = self._filter_if_available(candidates, "companions", companions)
        candidates = self._filter_if_available(candidates, "pace", pace)

        if theme != "Any":
            theme_columns = [
                col for col in [
                    "primary_theme", "secondary_theme", "destination_theme_profile", self.text_col
                ] if col in candidates.columns
            ]
            if theme_columns:
                mask = pd.Series(False, index=candidates.index)
                for col in theme_columns:
                    mask = mask | candidates[col].astype(str).str.contains(
                        theme, case=False, regex=False, na=False
                    )
                if mask.any():
                    candidates = candidates[mask]

        if candidates.empty:
            candidates = original
            notices.append("Preferences were too restrictive; ranking the full dataset for alternatives.")

        query = (
            f"Destination: {destination}. Duration: {days} days. "
            f"Budget category: {budget}. Travelling with: {companions}. "
            f"Interest: {theme}. Travel pace: {pace}. "
            "Return a relevant coherent day-wise travel plan."
        )

        indices = candidates.index.to_list()
        query_embedding = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)
        scores = cosine_similarity(query_embedding, self.embeddings[indices])[0]
        ranked = candidates.copy()
        ranked["match_score"] = scores
        ranked = ranked.sort_values("match_score", ascending=False).head(top_k)

        output = []
        for _, row in ranked.iterrows():
            output.append({
                "destination": str(row.get("destination", "")),
                "duration_days": str(row.get("duration_days", "")),
                "budget": str(row.get("budget", "")),
                "companions": str(row.get("companions", "")),
                "pace": str(row.get("pace", "")),
                "daily_plan": str(row.get("daily_plan", "")),
                "trip_plan": str(row.get("trip_plan", "")),
                "match_score": round(float(row.get("match_score", 0)), 4),
            })

        return output, " ".join(notices)
