"""
Loads the curated CSV datasets (occupations, courses, skills taxonomy) into
memory once at process startup. All recommendation computation downstream
happens live, per-request, against these in-memory frames — nothing here is
a pre-computed recommendation.
"""
from __future__ import annotations
import os
from functools import lru_cache
from typing import Dict, List

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _parse_skill_weights(cell: str) -> Dict[str, int]:
    """'Python:5;SQL:3' -> {'Python': 5, 'SQL': 3}"""
    out = {}
    if not isinstance(cell, str) or not cell.strip():
        return out
    for part in cell.split(";"):
        if ":" in part:
            name, weight = part.rsplit(":", 1)
            try:
                out[name.strip()] = int(weight)
            except ValueError:
                continue
    return out


def _parse_skill_list(cell: str) -> List[str]:
    if not isinstance(cell, str) or not cell.strip():
        return []
    return [s.strip() for s in cell.split(";") if s.strip()]


def _parse_pipe_list(cell: str) -> List[str]:
    if not isinstance(cell, str) or not cell.strip():
        return []
    return [s.strip() for s in cell.split("|") if s.strip()]


@lru_cache(maxsize=1)
def load_occupations() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_DIR, "occupations.csv"))
    df["skill_weights"] = df["skills"].apply(_parse_skill_weights)
    df["interest_tags"] = df["interests"].apply(_parse_pipe_list)
    # a flattened "skill document" used for TF-IDF (skill mentioned N times ~ weight)
    df["skill_document"] = df["skill_weights"].apply(
        lambda d: " ".join(
            (name.replace(" ", "_").replace("/", "_").replace("&", "and") + " ") * max(weight, 1)
            for name, weight in d.items()
        )
    )
    return df


@lru_cache(maxsize=1)
def load_courses() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_DIR, "courses.csv"))
    df["skill_list"] = df["skills"].apply(_parse_skill_list)
    df["skill_document"] = df["skill_list"].apply(
        lambda skills: " ".join(s.replace(" ", "_").replace("/", "_").replace("&", "and") for s in skills)
    )
    return df


@lru_cache(maxsize=1)
def load_skills_taxonomy() -> List[str]:
    df = pd.read_csv(os.path.join(DATA_DIR, "skills_taxonomy.csv"))
    return sorted(df["skill"].tolist())


@lru_cache(maxsize=1)
def all_interest_tags() -> List[str]:
    occs = load_occupations()
    tags = set()
    for row in occs["interest_tags"]:
        tags.update(row)
    return sorted(tags)
