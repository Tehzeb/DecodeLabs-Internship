"""
Skill-Gap Scoring layer.

Given a target occupation's weighted required-skill map and the user's actual
skills, computes which required skills are covered vs. missing, and an
importance-weighted coverage percentage. This is what a target's raw
similarity score can't tell you on its own: *which specific skills* to close
next, and how much each one matters for that specific role.
"""
from __future__ import annotations
from typing import Dict, List, Tuple

from app.models.schemas import SkillGapEntry


def _normalize(skill: str) -> str:
    return skill.strip().lower()


def compute_skill_gap(
    required_skills: Dict[str, int], user_skills: List[str]
) -> Tuple[List[str], List[str], float, List[SkillGapEntry]]:
    user_set = {_normalize(s) for s in user_skills}

    matched, missing = [], []
    breakdown: List[SkillGapEntry] = []
    total_weight = 0
    covered_weight = 0

    for skill, weight in sorted(required_skills.items(), key=lambda kv: -kv[1]):
        total_weight += weight
        has_it = _normalize(skill) in user_set
        if has_it:
            matched.append(skill)
            covered_weight += weight
        else:
            missing.append(skill)
        breakdown.append(SkillGapEntry(skill=skill, importance=weight, has_skill=has_it))

    coverage_pct = round((covered_weight / total_weight) * 100, 1) if total_weight else 0.0
    return matched, missing, coverage_pct, breakdown
