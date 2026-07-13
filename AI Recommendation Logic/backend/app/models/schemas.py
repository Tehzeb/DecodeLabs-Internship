from typing import List, Optional
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    skills: List[str] = Field(..., min_items=1, description="Skills the user already has")
    interests: List[str] = Field(default_factory=list, description="Interest tags, e.g. 'cybersecurity'")
    experience_years: float = Field(0, ge=0, le=40, description="Years of relevant experience")
    target_role: Optional[str] = Field(None, description="Optional: a specific role the user wants scored")


class SkillGapEntry(BaseModel):
    skill: str
    importance: int
    has_skill: bool


class CareerMatch(BaseModel):
    soc: str
    title: str
    category: str
    description: str
    salary_low: int
    salary_high: int
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    skill_coverage_pct: float
    skill_breakdown: List[SkillGapEntry]
    interests: List[str]


class CourseRecommendation(BaseModel):
    course_id: str
    title: str
    provider: str
    level: str
    duration_weeks: int
    rating: float
    enrolled_k: float
    url: str
    covers_missing_skills: List[str]
    relevance_score: float


class SimilarPath(BaseModel):
    title: str
    category: str
    shared_skill_ratio: float
    reason: str


class RecommendationResponse(BaseModel):
    generated_at: str
    input_echo: UserProfile
    top_careers: List[CareerMatch]
    focus_career: CareerMatch
    recommended_courses: List[CourseRecommendation]
    similar_learner_paths: List[SimilarPath]
    method_notes: dict
