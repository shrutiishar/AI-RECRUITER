from datetime import datetime
from taxonomy.constants import PROFICIENCY_SCORE


# ==========================================================
# Skill Utilities
# ==========================================================

def skill_map(candidate):
    """
    Converts skill list into a dictionary.

    {
        "Python": {...},
        "TensorFlow": {...}
    }
    """

    skills = {}

    for skill in candidate.get("skills", []):

        name = skill.get("name")

        if not name:
            continue

        skills[name] = skill

    return skills


# ==========================================================
# Skill Proficiency
# ==========================================================

def candidate_skill_proficiency(candidate, skill_name):

    for skill in candidate.get("skills", []):

        if skill.get("name", "").lower() == skill_name.lower():

            return skill.get(
                "proficiency",
                "beginner"
            )

    return "beginner"


# ==========================================================
# Cluster Matching
# ==========================================================

def cluster_strength(candidate_skills, cluster):

    """
    Parameters
    ----------
    candidate_skills : dict
        Output of skill_map()

    cluster : set
        Skill cluster from taxonomy

    Returns
    -------
    score
    matched_skills
    """

    matched = []

    total = len(cluster)

    if total == 0:
        return 0.0, []

    score = 0.0

    for skill in cluster:

        if skill in candidate_skills:

            info = candidate_skills[skill]

            proficiency = info.get(
                "proficiency",
                "beginner"
            ).lower()

            prof_score = PROFICIENCY_SCORE.get(
                proficiency,
                0.25
            )

            months = info.get(
                "duration_months",
                0
            )

            duration_bonus = min(
                months / 36,
                1.0
            )

            final = (
                0.7 * prof_score
                +
                0.3 * duration_bonus
            )

            score += final

            matched.append(info)

    score /= total

    return min(score, 1.0), matched


# ==========================================================
# Candidate Text
# ==========================================================

def full_text_blob(candidate):

    pieces = []

    profile = candidate.get("profile", {})

    pieces.append(
        profile.get("headline", "")
    )

    pieces.append(
        profile.get("summary", "")
    )

    pieces.append(
        profile.get("current_title", "")
    )

    pieces.append(
        profile.get("current_company", "")
    )

    # Skills

    for skill in candidate.get("skills", []):

        pieces.append(
            skill.get("name", "")
        )

    # Career

    for job in candidate.get(
        "career_history",
        []
    ):

        pieces.append(
            job.get("title", "")
        )

        pieces.append(
            job.get("company", "")
        )

        pieces.append(
            job.get("description", "")
        )

    return " ".join(

        str(x)

        for x in pieces

        if x

    ).lower()


# ==========================================================
# Parse Dates
# ==========================================================

def parse_date(value):

    if not value:
        return None

    formats = [

        "%Y-%m-%d",

        "%d-%m-%Y",

        "%Y/%m/%d",

        "%d/%m/%Y"

    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).date()

        except Exception:

            pass

    return None


# ==========================================================
# Normalize Text
# ==========================================================

def normalize(text):

    if text is None:
        return ""

    return " ".join(

        str(text)

        .lower()

        .strip()

        .split()

    )


# ==========================================================
# Experience
# ==========================================================

def total_experience_months(candidate):

    total = 0

    for job in candidate.get(
        "career_history",
        []
    ):

        total += job.get(
            "duration_months",
            0
        )

    return total


# ==========================================================
# Current Job
# ==========================================================

def current_job(candidate):

    for job in candidate.get(
        "career_history",
        []
    ):

        if job.get("is_current"):

            return job

    return None


# ==========================================================
# Skill Exists
# ==========================================================

def has_skill(candidate, skill):

    skill = skill.lower()

    for s in candidate.get(
        "skills",
        []
    ):

        if s.get(
            "name",
            ""
        ).lower() == skill:

            return True

    return False


# ==========================================================
# Multiple Skills
# ==========================================================

def has_any_skill(candidate, skills):

    existing = {

        s.get("name", "").lower()

        for s in candidate.get(
            "skills",
            []
        )

    }

    return bool(

        existing &

        {

            x.lower()

            for x in skills

        }

    )


# ==========================================================
# Average Proficiency
# ==========================================================

def average_skill_score(candidate):

    scores = []

    for skill in candidate.get(
        "skills",
        []
    ):

        prof = skill.get(
            "proficiency",
            "beginner"
        ).lower()

        scores.append(

            PROFICIENCY_SCORE.get(
                prof,
                0.25
            )

        )

    if not scores:

        return 0

    return sum(scores) / len(scores)


# ==========================================================
# Safe Division
# ==========================================================

def safe_divide(a, b):

    if b == 0:

        return 0

    return a / b
