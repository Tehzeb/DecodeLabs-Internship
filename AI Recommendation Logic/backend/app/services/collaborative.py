"""
'Learners with a similar profile also pursued...' layer.

HONEST NOTE ON METHOD: there is no public dataset of real people's actual
career/course choices tied to this exact task, so true user-user collaborative
filtering (the Netflix-style "users who rated X also rated Y") is not possible
using only real, publicly available data here. Building that layer on invented
user-interaction logs would mean the whole "similar learners" feature was
fake data wearing a real-sounding name.

Instead this module implements an honestly-labeled **proxy**: it treats each
occupation's real, weighted skill profile as a vector and finds the nearest
*occupations* in that skill space (cosine similarity) — i.e. "career paths
that need an overlapping skillset to the one you just matched with, which is
the same signal a population of similar learners would produce in aggregate."
The API response always tags this as `"method": "proxy-cf-skill-neighbors"`
so the frontend can (and does) disclose it rather than imply it came from
real user logs.
"""
from __future__ import annotations
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.data_loader import load_occupations


def similar_career_paths(anchor_soc: str, top_n: int = 3) -> List[dict]:
    occupations = load_occupations().copy()
    if anchor_soc not in occupations["soc"].values:
        return []

    vectorizer = TfidfVectorizer(token_pattern=r"[^\s]+")
    tfidf_matrix = vectorizer.fit_transform(occupations["skill_document"])

    anchor_idx = occupations.index[occupations["soc"] == anchor_soc][0]
    similarities = cosine_similarity(tfidf_matrix[anchor_idx], tfidf_matrix).flatten()

    occupations["neighbor_score"] = similarities
    neighbors = (
        occupations[occupations["soc"] != anchor_soc]
        .sort_values("neighbor_score", ascending=False)
        .head(top_n)
    )

    anchor_skills = set(occupations.loc[anchor_idx, "skill_weights"].keys())
    results = []
    for _, row in neighbors.iterrows():
        neighbor_skills = set(row["skill_weights"].keys())
        overlap = anchor_skills & neighbor_skills
        ratio = round(len(overlap) / max(len(anchor_skills | neighbor_skills), 1), 2)
        results.append({
            "title": row["title"],
            "category": row["category"],
            "shared_skill_ratio": ratio,
            "reason": (
                f"Shares {len(overlap)} core skill(s) with your top match "
                f"({', '.join(sorted(overlap)[:3])}{'…' if len(overlap) > 3 else ''}) — "
                "professionals who build one skillset commonly branch into the other."
            ),
        })
    return results
