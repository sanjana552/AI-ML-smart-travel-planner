import re
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer, util


class TripMatcher:
    def __init__(self, csv_or_df=None):
        """
        Initializes the TripMatcher using the local Triip_HF_v4_10k.csv dataset.
        csv_or_df can be a file path string/Path or an existing pandas DataFrame.
        """
        if csv_or_df is None or isinstance(csv_or_df, (str, Path)):
            if csv_or_df is None:
                csv_path = Path(__file__).resolve().parent.parent / "data" / "Triip_HF_v4_10k.csv"
            else:
                csv_path = Path(csv_or_df)

            if not csv_path.exists():
                raise FileNotFoundError(f"Dataset CSV not found at: {csv_path}")

            print(f"Loading local dataset from: {csv_path}")
            raw_df = pd.read_csv(csv_path)
        elif isinstance(csv_or_df, pd.DataFrame):
            raw_df = csv_or_df
        else:
            raise TypeError("csv_or_df must be a path or a pandas DataFrame")

        self.df = self._parse_dataset(raw_df)
        self.destinations_list = sorted(self.df["destination"].unique().tolist())
        print(f"Loaded and parsed {len(self.df)} records across {len(self.destinations_list)} unique destinations.")

        # Common destination aliases and spelling variants in India
        self.aliases = {
            "bengaluru": "Bangalore",
            "bangalore": "Bangalore",
            "bombay": "Mumbai",
            "mumbai": "Mumbai",
            "calcutta": "Kolkata",
            "kolkata": "Kolkata",
            "madras": "Chennai",
            "chennai": "Chennai",
            "new delhi": "Delhi",
            "delhi": "Delhi",
            "ncr": "Delhi",
            "banaras": "Varanasi",
            "kashi": "Varanasi",
            "varanasi": "Varanasi",
            "trivandrum": "Thiruvananthapuram",
            "thiruvananthapuram": "Thiruvananthapuram",
            "puducherry": "Pondicherry",
            "pondicherry": "Pondicherry",
            "panaji": "Goa",
            "north goa": "Goa",
            "south goa": "Goa",
            "goa": "Goa",
            "visakhapatnam": "Vizag",
            "vizag": "Vizag",
            "dharamsala": "Dharamshala",
            "mcleod ganj": "Mcleodganj",
            "mcleodganj": "Mcleodganj",
            "rann of kutch": "Rann of Kutch",
            "kutch": "Rann of Kutch",
            "mount abu": "Mount Abu"
        }

        # Build fast destination index
        self.dest_index = {}
        for idx, dest in enumerate(self.df["destination"]):
            self.dest_index.setdefault(dest.casefold(), []).append(idx)

        # Sentence transformer model for semantic matching
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Semantic travel model loaded successfully.")

    def _parse_dataset(self, df):
        """
        Parses instruction, input, and output columns from the dataset.
        Extracts duration days, destination, theme, companion, budget tier,
        and converts markdown itinerary into a structured daily_plan.
        """
        input_pattern = re.compile(
            r"A\s+(\d+)-day\s+(.*?)\s+trip\s+to\s+(.*?)\s+for\s+(?:a\s+)?(.*?)\s+on\s+a\s+(.*?)\s+budget",
            re.IGNORECASE
        )

        rows = []
        for idx, row in df.iterrows():
            input_text = str(row.get("input", "")).strip()
            output_text = str(row.get("output", "")).strip()

            m = input_pattern.search(input_text)
            if m:
                days, theme_season, dest, companions, budget_tier = m.groups()
                days = int(days)
                dest = dest.strip()
                theme_season = theme_season.strip()
                companions = companions.strip()
                budget_tier = budget_tier.strip()
            else:
                days_match = re.search(r"(\d+)-day", input_text)
                days = int(days_match.group(1)) if days_match else 3
                dest_match = re.search(r"trip to\s+([A-Za-z\s]+?)\s+for", input_text)
                dest = dest_match.group(1).strip() if dest_match else "India"
                theme_season = "leisure"
                companions = "travelers"
                budget_tier = "mid-range"

            # Parse markdown output into structured daily_plan
            daily_plan, note = self._parse_markdown(output_text, dest, days)

            search_text = (
                f"Travel to {dest}. {days} days trip. {theme_season}. "
                f"For {companions}. Budget style: {budget_tier}."
            )

            rows.append({
                "original_idx": idx,
                "days": days,
                "destination": dest,
                "theme_season": theme_season,
                "companions": companions,
                "budget_tier": budget_tier,
                "input": input_text,
                "output": output_text,
                "raw_itinerary": output_text,
                "daily_plan": daily_plan,
                "note": note,
                "search_text": search_text
            })

        return pd.DataFrame(rows)

    def _parse_markdown(self, markdown_text, destination, days):
        """
        Parses Markdown output into daily_plan list and continuing note.
        """
        day_blocks = re.split(r"(?=###\s*Day\s*\d+)", markdown_text, flags=re.IGNORECASE)
        day_header_re = re.compile(r"^###\s*Day\s*(\d+)(?::\s*(.*))?$", re.MULTILINE | re.IGNORECASE)
        stop_re = re.compile(r"[-*]\s+\*\*([^(:]+)(?:\(([^)]+)\))?\s*:\*\*\s*(.*)", re.IGNORECASE)

        daily_plan = []
        note_text = ""

        for block in day_blocks:
            block = block.strip()
            if not block:
                continue

            header_match = day_header_re.search(block)
            if not header_match:
                if "note:" in block.lower():
                    note_text = block.strip("*_ \n")
                continue

            day_num = int(header_match.group(1))
            title = (
                header_match.group(2).strip()
                if header_match.group(2)
                else f"Day {day_num}: Exploration in {destination}"
            )

            stops = []
            for line in block.split("\n"):
                line = line.strip()
                if line.lower().startswith("*note:") or line.lower().startswith("note:"):
                    note_text = line.strip("*_ \n")
                    continue

                sm = stop_re.search(line)
                if sm:
                    period = sm.group(1).strip()
                    time_val = sm.group(2).strip() if sm.group(2) else ""
                    activity = sm.group(3).strip()

                    place = self._extract_place_title(activity, period, destination)

                    stops.append({
                        "period": period,
                        "time": time_val or period,
                        "place": place,
                        "activity": activity,
                        "estimated_cost": None,
                        "travel_duration": None
                    })

            if stops:
                daily_plan.append({
                    "day": day_num,
                    "title": title,
                    "stops": stops,
                    "estimated_day_cost": None
                })

        return daily_plan, note_text

    def _extract_place_title(self, activity, period, destination):
        act_clean = re.sub(
            r"^(Start with|Begin with|Explore|Visit|Head to)\s+",
            "",
            activity,
            flags=re.IGNORECASE
        ).strip()
        first_clause = re.split(r"[;.,]|\s+focusing on\s+|\s+during\s+", act_clean)[0].strip()
        if len(first_clause) > 40:
            first_clause = first_clause[:37] + "..."
        if first_clause:
            return first_clause.capitalize()
        return f"{period} in {destination}"

    def resolve_destination(self, user_dest):
        query = str(user_dest or "").strip().casefold()
        if not query:
            return None

        if query in self.aliases:
            return self.aliases[query]

        # Exact match
        for dest in self.dest_index.keys():
            if dest == query:
                return self.df.loc[self.dest_index[dest][0], "destination"]

        # Partial substring match (requires at least 3 chars)
        if len(query) >= 3:
            for dest in self.dest_index.keys():
                if query in dest or dest in query:
                    return self.df.loc[self.dest_index[dest][0], "destination"]

        return None

    def recommend(
        self,
        destination,
        days,
        budget=None,
        companions="Any",
        theme="Any",
        pace="Any",
        top_k=3
    ):
        """
        Finds matching dataset itineraries for the destination and duration,
        and ranks them using semantic similarity.
        """
        destination_str = str(destination or "").strip()
        if not destination_str:
            return [], "Please enter a destination."

        matched_dest = self.resolve_destination(destination_str)
        if not matched_dest:
            return [], (
                f"Destination '{destination_str}' is not present in the dataset. "
                "Use the AI itinerary fallback."
            )

        candidate_indices = self.dest_index.get(matched_dest.casefold(), [])
        if not candidate_indices:
            return [], f"No dataset records found for '{matched_dest}'."

        candidates = self.df.iloc[candidate_indices].copy()

        # Prioritize exact duration match
        exact_days = candidates[candidates["days"] == int(days)]
        if not exact_days.empty:
            candidates = exact_days
        else:
            candidates["days_diff"] = (candidates["days"] - int(days)).abs()
            min_diff = candidates["days_diff"].min()
            # If the closest available itinerary is within 3 days, consider it;
            # otherwise allow AI fallback to generate an itinerary for the exact day count.
            if min_diff <= 3:
                candidates = candidates[candidates["days_diff"] == min_diff]
            else:
                return [], (
                    f"No dataset itinerary close to {days} days for {matched_dest}. "
                    "Use the AI itinerary fallback."
                )

        # Semantic query
        query = (
            f"Travel to {matched_dest}. Trip duration: {days} days. "
            f"Budget: {budget if budget else 'standard'} INR. "
            f"Travelling with: {companions}. Interests: {theme}. Preferred pace: {pace}."
        )

        query_emb = self.model.encode(query, convert_to_tensor=True)
        candidate_texts = candidates["search_text"].tolist()
        cand_embs = self.model.encode(candidate_texts, convert_to_tensor=True)

        cos_scores = util.cos_sim(query_emb, cand_embs)[0].cpu().tolist()
        candidates["match_score"] = [round(float(s), 4) for s in cos_scores]

        ranked = candidates.sort_values("match_score", ascending=False).head(top_k)

        results = []
        for _, row in ranked.iterrows():
            results.append({
                "destination": row["destination"],
                "duration_days": int(row["days"]),
                "days": int(row["days"]),
                "budget_tier": row["budget_tier"],
                "theme": row["theme_season"],
                "companions": row["companions"],
                "pace": pace,
                "daily_plan": row["daily_plan"],
                "raw_itinerary": row.get("raw_itinerary", row.get("output", "")),
                "trip_plan": row.get("raw_itinerary", row.get("output", "")),
                "notice": row["note"] or f"Curated itinerary from Triip dataset for {row['destination']}.",
                "match_score": row["match_score"],
                "source": "Dataset Recommendation"
            })

        return results, f"Found {len(results)} matching dataset itinerary(s) for {matched_dest}."
