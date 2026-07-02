from datetime import datetime


def parse_date(date_str):
    """
    Safely parse YYYY-MM-DD date strings.
    """
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def skill_map(candidate):
    """
    Returns:
    {
        "Python": {...},
        "TensorFlow": {...}
    }
    """
    return {
        skill["name"]: skill
        for skill in candidate.get("skills", [])
    }


def skill_names(candidate):
    """
    Returns only the skill names.
    """
    return set(skill_map(candidate).keys())


def candidate_skill_proficiency(candidate, skill_name):
    """
    Returns proficiency of a particular skill.
    """
    for skill in candidate.get("skills", []):

        if skill["name"] == skill_name:
            return skill.get("proficiency")

    return None


def full_text_blob(candidate):
    """
    Combine every textual field so we can search
    production/research/etc.
    """

    text = []

    profile = candidate.get("profile", {})

    text.append(profile.get("headline", ""))
    text.append(profile.get("summary", ""))

    for job in candidate.get("career_history", []):

        text.append(job.get("title", ""))
        text.append(job.get("description", ""))

    return " ".join(text).lower()


def cluster_hits(skill_dictionary, cluster):
    """
    Returns every skill inside one taxonomy cluster.
    """

    hits = []

    for name in cluster:

        if name in skill_dictionary:
            hits.append(skill_dictionary[name])

    hits.sort(
        key=lambda x: x.get("duration_months", 0),
        reverse=True
    )

    return hits


def cluster_strength(skill_dictionary, cluster):
    """
    Recruiter-like scoring.

    Doesn't just check presence.

    Uses

    • duration
    • proficiency
    • breadth
    """

    hits = cluster_hits(skill_dictionary, cluster)

    if len(hits) == 0:
        return 0.0, []

    proficiency_weight = {

        "beginner": 0.40,
        "intermediate": 0.65,
        "advanced": 0.85,
        "expert": 1.00

    }

    best = hits[0]

    duration = min(
        best.get("duration_months", 0) / 24,
        1.0
    )

    proficiency = proficiency_weight.get(
        best.get("proficiency", "intermediate"),
        0.6
    )

    breadth_bonus = min(
        (len(hits) - 1) * 0.15,
        0.30
    )

    score = (

        0.5 * duration

        +

        0.5 * proficiency

        +

        breadth_bonus

    )

    return min(score, 1.0), hits
