# BiteWise AI

AI-powered restaurant recommendation system inspired by Zomato. Users enter preferences (location, budget, cuisine, rating, and notes), the backend filters a real restaurant dataset, and OpenAI ranks and explains the best matches. Results are shown in a **Next.js** web app with a FastAPI backend.

**Repository:** [github.com/tejas2904-RM/BiteWise-Ai](https://github.com/tejas2904-RM/BiteWise-Ai)

## Features

- Preference-based search (location, budget tier, cuisine, minimum rating, free-text notes)
- Filtering over 50,000+ restaurants from the [Zomato Hugging Face dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- OpenAI-powered ranking and explanations (`gpt-4o-mini` by default)
- Rule-based fallback ranking when OpenAI is unavailable
- Deduplicated results with backfill to return up to 5 unique recommendations
- BiteWise UI: landing, search, loading, curated results, restaurant detail, empty and error states
- Production deployment on **Render** (API) and **Vercel** (frontend)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data / ML pipeline | Python, pandas, pyarrow, Hugging Face `datasets` |
| LLM | OpenAI API (`openai` SDK) |
| Backend API | FastAPI, Uvicorn |
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend hosting | [Render](https://render.com) |
| Frontend hosting | [Vercel](https://vercel.com) |

## Architecture

The project is organized in phases, each in its own folder:

```
User (Browser)
      │
      ▼
phase7_frontend/          Next.js UI
      │
      ▼
phase6_backend_api/       FastAPI REST API
      │
      ├── phase2_user_input/          Preference validation
      ├── phase3_integration_layer/   Filter + prompt builder
      ├── phase4_recommendation_engine/  OpenAI + fallback ranker
      └── phase5_response_contract/   Shared API schemas
      │
      ▼
phase1_data_ingestion/    Restaurant dataset (parquet)
```

| Phase | Folder | Purpose |
|-------|--------|---------|
| 1 | `phase1_data_ingestion/` | Load and preprocess Zomato data |
| 2 | `phase2_user_input/` | User preference models and validation |
| 3 | `phase3_integration_layer/` | Filter restaurants, build LLM prompt |
| 4 | `phase4_recommendation_engine/` | OpenAI ranking + fallback |
| 5 | `phase5_response_contract/` | Pydantic models and JSON schemas |
| 6 | `phase6_backend_api/` | FastAPI backend |
| 7 | `phase7_frontend/` | Next.js frontend |
| 8 | `phase8_backend_deploy/` | Render deployment scripts |
| 9 | `phase9_frontend_deploy/` | Vercel deployment config |

See [Docs/PhaseWiseArchitecture.md](Docs/PhaseWiseArchitecture.md) for full design details.

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **OpenAI API key** (for AI recommendations; fallback mode works without it)
- Git

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/tejas2904-RM/BiteWise-Ai.git
cd BiteWise-Ai
```

### 2. Generate restaurant data (Phase 1)

```bash
cd phase1_data_ingestion
pip install -r requirements.txt
python main.py
```

This downloads the dataset from Hugging Face and writes:

`phase1_data_ingestion/data/processed/restaurants.parquet`

### 3. Configure OpenAI (Phase 4)

```bash
cd phase4_recommendation_engine
cp .env.example .env
```

Edit `.env` and set your key:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 4. Start the backend (Phase 6)

```bash
cd phase6_backend_api
pip install -r requirements.txt
cp .env.example .env   # optional for local overrides
python main.py
```

API runs at **http://127.0.0.1:8000**

- Health check: `GET /health`
- Interactive docs: http://127.0.0.1:8000/docs

### 5. Start the frontend (Phase 7)

```bash
cd phase7_frontend
npm install
cp .env.local.example .env.local
npm run dev
```

App runs at **http://localhost:3000**

Set in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health and restaurant count |
| `POST` | `/api/recommendations` | Get ranked recommendations |
| `GET` | `/api/restaurants/{id}` | Restaurant details |
| `GET` | `/api/search/history` | Recent searches (in-memory) |

**Example recommendation request:**

```bash
curl -X POST "http://127.0.0.1:8000/api/recommendations?top_n=5" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Bangalore",
    "budget": "medium",
    "cuisine": "Chinese",
    "min_rating": 4.0,
    "additional_notes": "family-friendly"
  }'
```

Use `?fallback_only=true` to skip OpenAI and test rule-based ranking.

## Environment Variables

### Backend (`phase6_backend_api` / Render)

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | Model name (default: `gpt-4o-mini`) |
| `DATA_PATH` | Path to `restaurants.parquet` |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins |
| `CORS_ALLOW_VERCEL_PREVIEWS` | Allow `*.vercel.app` preview URLs (`true`/`false`) |

### Frontend (`phase7_frontend` / Vercel)

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Render API base URL (no trailing slash) |

Templates: `phase8_backend_deploy/.env.render.example`, `phase9_frontend_deploy/.env.vercel.example`

## Deployment

### Backend — Render (Phase 8)

1. Push the repo to GitHub.
2. In [Render](https://render.com), create a **Blueprint** from the repository.
3. The root `render.yaml` configures the `bitewise-api` web service.
4. Set `OPENAI_API_KEY` in the Render dashboard.
5. Verify: `GET https://<your-service>.onrender.com/health`

The build step runs `ensure_data.py` to generate restaurant data if the parquet file is not in the repo.

### Frontend — Vercel (Phase 9)

1. Import the GitHub repo in [Vercel](https://vercel.com).
2. Set **Root Directory** to `phase7_frontend`.
3. Add `NEXT_PUBLIC_API_URL` pointing to your Render API URL.
4. Deploy.

After the first Vercel deploy, update Render `CORS_ORIGINS` with your production Vercel URL if needed.

## Running Tests

```bash
# Phase 1
cd phase1_data_ingestion && python -m pytest tests/ -q

# Phase 3
cd phase3_integration_layer && python -m pytest tests/ -q

# Phase 4
cd phase4_recommendation_engine && python -m pytest tests/ -q

# Phase 6 (API)
cd phase6_backend_api && python -m pytest tests/ -q

# Phase 8 / 9 (deploy config)
cd phase8_backend_deploy && python -m pytest tests/ -q
cd phase9_frontend_deploy && python -m pytest tests/ -q
```

## Documentation

- [Problem Statement](Docs/Problemstatment.md)
- [Phase-Wise Architecture](Docs/PhaseWiseArchitecture.md)
- [Google Stitch UI Prompts](Docs/GoogleStitchUIPrompts.md)

## Security Notes

- Never commit `.env` files or API keys.
- `phase4_recommendation_engine/.env` and `phase7_frontend/.env.local` are gitignored.
- Store production secrets only in Render and Vercel environment settings.

## License

This project was built as an educational / portfolio application. Check repository settings for license details.
