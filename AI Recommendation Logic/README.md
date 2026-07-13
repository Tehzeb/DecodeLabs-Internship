# VANTAGE — Personalized Career & Skill Path Advisor

**AI Recommendation Logic — Internship Project (DecodeLabs)**

A hybrid recommendation system that takes a user's real skills, years of
experience, and interests and computes — live, on every request — the tech
careers they're the best fit for, exactly which skills are missing for each,
and the specific courses that close those gaps fastest.

---

## 1. What "hybrid" means here

| Layer | Technique | What it answers |
|---|---|---|
| **1. Career matching** | Content-Based Filtering — TF-IDF vectorization + cosine similarity | "Which occupations best match *this* skill/interest profile?" |
| **2. Skill-Gap Scoring** | Importance-weighted coverage scoring against O*NET-informed skill weights | "Of the skills that role needs, which do I have — and how much does each one matter?" |
| **3. Course recommendation** | Content-Based Filtering again, this time TF-IDF over the *missing-skill vector* vs. the course catalog | "Which real courses cover my specific gaps, ranked by relevance and rating?" |
| **4. Similar-path suggestions** | Proxy Collaborative Filtering — skill-space nearest-neighbor occupations | "What do people who need a similar skillset often pursue next?" |

**Every one of these is computed fresh per request** against the in-memory
dataset — nothing is a lookup from a precomputed table. Submit the same
profile twice and you'll get the same answer because the math is
deterministic, not because it was cached.

### An honest note on the collaborative-filtering layer
True user-user collaborative filtering ("users like you also chose X") needs
a dataset of real people's real choices. No public dataset like that exists
for this exact task — inventing fake user logs to power it would mean the
"real data only" requirement was being quietly violated under the hood. So
this project implements a clearly-labeled **proxy**: it finds the nearest
occupations in real skill-vector space and presents that as the "similar
learners" signal. The API tags this explicitly as
`"method": "proxy-cf-skill-neighbors"` and the UI discloses it in plain
language rather than implying it came from real interaction logs. See
`backend/app/services/collaborative.py` for the full reasoning.

---

## 2. Data

Both datasets are curated, real-world extracts (not synthetic/fabricated),
built by the scripts in `backend/app/data/`:

- **`occupations.csv`** — 20 tech occupations aligned to real
  **O\*NET-SOC** codes (U.S. Dept. of Labor, public domain, onetonline.org),
  with importance-weighted (1–5) required skills condensed from O\*NET's
  Skills/Technology-Skills ratings for the closest matching SOC codes.
- **`courses.csv`** — 61 real, currently/previously publicly-listed courses
  from Coursera, edX, Udemy and fast.ai (real titles, providers, levels),
  tagged against the same skills taxonomy.
- **`skills_taxonomy.csv`** — the unified list of ~59 skills used across
  both datasets, powering the autocomplete in the UI.

If you'd rather pull the full official datasets yourself:
- O\*NET database download: https://www.onetcenter.org/database.html
- Kaggle Coursera Courses dataset: https://www.kaggle.com/datasets/siddharthm1698/coursera-course-dataset

The data-loading code (`backend/app/services/data_loader.py`) reads plain
CSVs, so swapping in the full O\*NET/Kaggle files just means matching the
same column shape — no other code changes needed.

---

## 3. Architecture

```
career-advisor-ai/
├── backend/                     FastAPI service (Python)
│   ├── app/
│   │   ├── main.py               app entrypoint, CORS
│   │   ├── models/schemas.py     Pydantic request/response models
│   │   ├── routers/recommend.py  /api/recommend orchestration
│   │   ├── services/
│   │   │   ├── data_loader.py         loads CSVs → pandas
│   │   │   ├── content_recommender.py  TF-IDF + cosine similarity (careers & courses)
│   │   │   ├── skill_gap.py            weighted skill-gap scoring
│   │   │   └── collaborative.py        proxy CF (skill-space neighbors)
│   │   └── data/
│   │       ├── build_occupations.py    → generates occupations.csv
│   │       ├── build_courses.py        → generates courses.csv
│   │       ├── occupations.csv
│   │       ├── courses.csv
│   │       └── skills_taxonomy.csv
│   ├── requirements.txt
│   └── run.py
│
└── frontend/                    React 18 + Vite + Tailwind + Framer Motion
    └── src/
        ├── components/           Hero, ProfileForm, ConstellationViz,
        │                         CareerCard, SkillGapBars, CourseCard,
        │                         SimilarPaths, ResultsDashboard, Header, Loader
        ├── context/ThemeContext.jsx   light/dark mode (persisted)
        ├── api/client.js              typed API calls to FastAPI
        └── App.jsx
```

**API surface:**

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness + dataset row counts |
| GET | `/api/skills` | Skills taxonomy for autocomplete |
| GET | `/api/interests` | Interest tag list |
| POST | `/api/recommend` | The full hybrid pipeline, computed live |
| GET | `/docs` | Interactive Swagger UI (auto-generated by FastAPI) |

---

## 4. Design

The UI ("VANTAGE") is built around a navigation/flight-console metaphor —
you enter your position, it plots your course. The signature element is the
**skill constellation**: an animated SVG graph connecting your matched
skills through to each career, and each career out to what's still missing.
Full light and dark themes, both driven by the same CSS variable tokens.

---

## 5. Run it — see `SETUP_WINDOWS.md` for the full step-by-step.

Quick version, two terminals:

```powershell
# Terminal 1 — backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173**.
