from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import recommend

app = FastAPI(
    title="Career & Skill Path Advisor API",
    description=(
        "Hybrid AI recommendation engine: Content-Based Filtering (TF-IDF + cosine "
        "similarity) over a curated, O*NET-informed tech-occupation dataset, layered "
        "with weighted Skill-Gap Scoring and a proxy Collaborative-Filtering signal. "
        "Every recommendation is computed live from the submitted profile — nothing "
        "is looked up from a precomputed table."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router)


@app.get("/")
def root():
    return {"service": "career-advisor-api", "docs": "/docs"}
