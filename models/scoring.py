from __future__ import annotations

import re

from product_config import (
    SCORING_CORRECT_OUTCOME_POINTS,
    SCORING_EMPTY_RESULT_POINTS,
    SCORING_EXACT_SCORE_POINTS,
    SCORING_MISS_POINTS,
)


SCORE_RE = re.compile(r"^\s*(\d{1,2})\s*[-:]\s*(\d{1,2})\s*$")


def parse_score(score_text: object) -> tuple[int, int] | None:
    if score_text is None:
        return None
    text = str(score_text).strip()
    if not text or text.lower() in {"nan", "none", "tbd"}:
        return None
    match = SCORE_RE.match(text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def winner_from_score(score_text: object) -> str | None:
    score = parse_score(score_text)
    if score is None:
        return None
    side_a, side_b = score
    if side_a > side_b:
        return "A"
    if side_b > side_a:
        return "B"
    return "DRAW"


def score_prediction(prediction: object, result: object) -> int:
    result_score = parse_score(result)
    if result_score is None:
        return SCORING_EMPTY_RESULT_POINTS

    prediction_score = parse_score(prediction)
    if prediction_score is None:
        return SCORING_MISS_POINTS
    if prediction_score == result_score:
        return SCORING_EXACT_SCORE_POINTS
    if winner_from_score(prediction) == winner_from_score(result):
        return SCORING_CORRECT_OUTCOME_POINTS
    return SCORING_MISS_POINTS
