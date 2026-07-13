from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    UserProfile, RecommendationResponse, CareerMatch, CourseRecommendation, SimilarPath,
)
from app.services.data_loader import load_occupations, load_courses, load_skills_taxonomy, all_interest_tags
from app.services.content_recommender import rank_careers, rank_courses_for_gap
from app.services.skill_gap import compute_skill_gap
from app.services.collaborative import similar_career_paths

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/skills")
def get_skills():
    return {"skills": load_skills_taxonomy()}


@router.get("/interests")
def get_interests():
    return {"interests": all_interest_tags()}


@router.get("/health")
def health():
    occs = load_occupations()
    courses = load_courses()
    return {
        "status": "ok",
        "occupations_loaded": int(len(occs)),
        "courses_loaded": int(len(courses)),
    }


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(profile: UserProfile):
    if not profile.skills:
        raise HTTPException(status_code=400, detail="Provide at least one skill.")

    # 1) Content-Based Filtering — live TF-IDF + cosine similarity over occupations
    ranked = rank_careers(profile.skills, profile.interests, top_n=5)
    if ranked.empty:
        raise HTTPException(status_code=404, detail="No matching careers found for this profile.")

    top_careers = []
    for _, row in ranked.iterrows():
        matched, missing, coverage_pct, breakdown = compute_skill_gap(row["skill_weights"], profile.skills)
        top_careers.append(CareerMatch(
            soc=row["soc"], title=row["title"], category=row["category"],
            description=row["description"], salary_low=int(row["salary_low"]),
            salary_high=int(row["salary_high"]), match_score=float(row["match_score"]),
            matched_skills=matched, missing_skills=missing, skill_coverage_pct=coverage_pct,
            skill_breakdown=breakdown, interests=row["interest_tags"],
        ))

    # experience nudges score slightly for roles the user is already well-covered on,
    # reflecting that similarity alone doesn't capture "ready now vs needs years of runway"
    for c in top_careers:
        readiness_bonus = min(profile.experience_years * 0.4, 4.0) if c.skill_coverage_pct >= 50 else 0.0
        c.match_score = round(min(c.match_score + readiness_bonus, 100.0), 1)
    top_careers.sort(key=lambda c: c.match_score, reverse=True)

    focus_career = top_careers[0]
    if profile.target_role:
        for c in top_careers:
            if c.title.lower() == profile.target_role.lower():
                focus_career = c
                break

    # 2) Skill-Gap-driven course recommendations — live TF-IDF vs the focus career's missing skills
    course_df = rank_courses_for_gap(focus_career.missing_skills, top_n=6)
    recommended_courses = [
        CourseRecommendation(
            course_id=row["course_id"], title=row["title"], provider=row["provider"],
            level=row["level"], duration_weeks=int(row["duration_weeks"]), rating=float(row["rating"]),
            enrolled_k=float(row["enrolled_k"]), url=row["url"],
            covers_missing_skills=row["covered"], relevance_score=float(row["relevance_score"]),
        )
        for _, row in course_df.iterrows()
    ]

    # 3) Proxy collaborative filtering — "learners with a similar profile also pursued..."
    neighbors = similar_career_paths(focus_career.soc, top_n=3)
    similar_paths = [SimilarPath(**n) for n in neighbors]

    return RecommendationResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        input_echo=profile,
        top_careers=top_careers,
        focus_career=focus_career,
        recommended_courses=recommended_courses,
        similar_learner_paths=similar_paths,
        method_notes={
            "career_matching": "content-based-tfidf-cosine (computed live per request)",
            "skill_gap": "weighted-coverage (O*NET-informed importance weights)",
            "course_ranking": "content-based-tfidf-cosine against missing-skill vector",
            "similar_learners": "proxy-cf-skill-neighbors (see collaborative.py docstring — "
                                 "no real public user-interaction dataset exists for this task, "
                                 "so this is explicitly a skill-space neighbor proxy, not real logs)",
        },
    )
