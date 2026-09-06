import math
from datetime import datetime, timezone


def calculate_retention(last_practiced_at: str, stability: float) -> float:
    """
    Calculates current retention (0 to 1) using the forgetting curve:
    R(t) = e^(-t / S)

    last_practiced_at: ISO timestamp string of when the skill was last practiced
    stability: how resistant this skill is to decay (higher = forgotten slower)
    """
    if last_practiced_at is None:
        return 0.0

    last_practiced = datetime.fromisoformat(last_practiced_at)
    now = datetime.now(timezone.utc)

    elapsed_seconds = (now - last_practiced).total_seconds()
    elapsed_days = elapsed_seconds / 86400

    retention = math.exp(-elapsed_days / stability)
    return round(retention, 4)


def update_stability(current_stability: float, intensity: float, days_since_last_practice: float) -> float:
    """
    Increases stability after a practice event.
    Practicing after a reasonable gap (not cramming) increases stability more —
    this rewards spaced repetition over same-day repeated practice.
    """
    spacing_factor = min(days_since_last_practice / 7, 1.0)
    growth = intensity * spacing_factor * 0.5

    new_stability = current_stability * (1 + growth)
    return round(new_stability, 4)