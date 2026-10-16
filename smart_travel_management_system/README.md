# AI & ML Powered Smart Travel Planner

This is an initial, folder-organized prototype for the college project.

## Folder structure

```text
smart_travel_management_system/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/travel_routes.py
│   ├── services/recommendation_service.py
│   ├── ml/trip_matcher.py
│   └── data/README.md
└── README.md
```

## How it works

1. The frontend collects destination, duration, budget category, travel companions, interest, and pace.
2. The Python Flask backend receives the request.
3. The recommendation service loads trip plans from Hugging Face.
4. A pretrained sentence-embedding model plus cosine similarity ranks candidate plans.
5. The response includes the matching dataset plan and daily plan.

Important: this first version performs retrieval/ranking using a pretrained embedding model. It does not train a new model from scratch. The dataset contains existing trip plans, so the output is a recommended matching plan, not a guarantee of a feasible real-world itinerary. The budget is a dataset category unless actual cost values exist.

## Requirements

- Python 3.10 or 3.11 recommended
- Internet access on first run to download the dataset/model

## Run on Windows

Open a terminal in the `backend` folder:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

The API starts at `http://127.0.0.1:5000`.

Then open `frontend/index.html` in a browser. If the browser blocks local API requests, serve the frontend from its folder in another terminal:

```bash
python -m http.server 5500
```

Open `http://127.0.0.1:5500`.

## API endpoint

`POST /api/itinerary`

Example JSON:

```json
{
  "destination": "Jaipur",
  "days": 3,
  "budget": "Any",
  "companions": "Any",
  "theme": "History",
  "pace": "Any"
}
```

## Next planned milestones

- Dataset inspection and preprocessing report
- Evaluation and comparison of recommendation approaches
- Explicit validation that the final itinerary matches the requested number of days
- Actual expense estimation if reliable numeric cost data is available
- User authentication, MySQL persistence, expense tracking, charts
- Optional Generative AI itinerary narration
