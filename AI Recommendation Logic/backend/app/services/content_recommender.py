"""
Content-Based Filtering engine.

For every request, a fresh TF-IDF space is fit over (all occupation skill
documents + this user's skill document). This is intentional: nothing here
is pre-computed offline. The moment a user submits their profile, we vectorize
their exact skill set against the current dataset and score cosine similarity
live. Swap the CSVs for a live O*NET / Coursera API pull and the same code
path keeps working unchanged.
"""
from __future__ import annotations
from typing import List, Dict

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.data_loader import load_occupations, load_courses


def _tokenize_skill(name: str) -> str:
    return name.strip().replace(" ", "_").replace("/", "_").replace("&", "and")


def build_user_document(skills: List[str], interests: List[str]) -> str:
    skill_tokens = " ".join(_tokenize_skill(s) for s in skills)
    # interests get lighter weight (repeated once) vs skills which anchor the match
    interest_tokens = " ".join(_tokenize_skill(i) for i in interests)
    return f"{skill_tokens} {skill_tokens} {interest_tokens}".strip()


def rank_careers(skills: List[str], interests: List[str], top_n: int = 5) -> pd.DataFrame:
    """Live TF-IDF + cosine similarity ranking of occupations against a user profile."""
    occupations = load_occupations().copy()
    user_doc = build_user_document(skills, interests)

    corpus = occupations["skill_document"].tolist() + [user_doc]
    vectorizer = TfidfVectorizer(token_pattern=r"[^\s]+")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    user_vector = tfidf_matrix[-1]
    occupation_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(user_vector, occupation_vectors).flatten()
    occupations["match_score"] = (similarities * 100).round(1)

    return occupations.sort_values("match_score", ascending=False).head(top_n).reset_index(drop=True)


def rank_courses_for_gap(missing_skills: List[str], top_n: int = 6) -> pd.DataFrame:
    """Live TF-IDF + cosine similarity ranking of courses against a skill-gap document."""
    courses = load_courses().copy()
    if not missing_skills:
        courses["relevance_score"] = 0.0
        courses["covered"] = [[] for _ in range(len(courses))]
        return courses.head(0)

    gap_doc = " ".join(_tokenize_skill(s) for s in missing_skills)
    corpus = courses["skill_document"].tolist() + [gap_doc]
    vectorizer = TfidfVectorizer(token_pattern=r"[^\s]+")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    gap_vector = tfidf_matrix[-1]
    course_vectors = tfidf_matrix[:-1]
    similarities = cosine_similarity(gap_vector, course_vectors).flatten()
    courses["relevance_score"] = (similarities * 100).round(1)

    missing_set = {s for s in missing_skills}
    courses["covered"] = courses["skill_list"].apply(lambda lst: [s for s in lst if s in missing_set])

    ranked = courses[courses["relevance_score"] > 0].sort_values(
        ["relevance_score", "rating"], ascending=[False, False]
    )
    return ranked.head(top_n).reset_index(drop=True)
