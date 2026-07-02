from taxonomy import (
    FRAMEWORK_WRAPPER_SKILLS,
    EMBEDDINGS_RETRIEVAL,
    VECTOR_DB_HYBRID_SEARCH,
    CONSULTING_FIRMS,
    CV_SPEECH_ROBOTICS,
    NLP_IR_SIGNAL,
)

from .helpers import skill_map


def do_not_want_check(candidate):
    """
    Soft penalties based on recruiter preferences.

    Returns
    -------
    multiplier
    flags
    """

    multiplier = 1.0
    flags = []

    career = candidate.get("career_history", [])

    skills = skill_map(candidate)
    skill_names = set(skills.keys())

    # --------------------------------------------------
    # Title Chasing
    # --------------------------------------------------

    short_roles = [

        job

        for job in career

        if job.get("duration_months", 999) <= 18

    ]

    promotion_words = [

        "junior",
        "senior",
        "lead",
        "staff",
        "principal"

    ]

    promotions = sum(

        1

        for job in career

        if any(

            word in job.get("title", "").lower()

            for word in promotion_words

        )

    )

    if (

        len(career) >= 3

        and

        len(short_roles) >= len(career) - 1

        and

        promotions >= 2

    ):

        flags.append(

            "Possible title chasing."

        )

        multiplier *= 0.55

    # --------------------------------------------------
    # Framework Enthusiast
    # --------------------------------------------------

    wrapper = skill_names & FRAMEWORK_WRAPPER_SKILLS

    retrieval = (

        EMBEDDINGS_RETRIEVAL

        |

        VECTOR_DB_HYBRID_SEARCH

    )

    retrieval = skill_names & retrieval

    github = (

        candidate

        .get("redrob_signals", {})

        .get("github_activity_score", 0)

    )

    if wrapper and not retrieval and github < 20:

        flags.append(

            "Only framework level AI experience."

        )

        multiplier *= 0.70

    # --------------------------------------------------
    # Consulting Only Career
    # --------------------------------------------------

    companies = {

        job.get("company")

        for job in career

    }

    companies.add(

        candidate

        .get("profile", {})

        .get("current_company")

    )

    if companies and companies.issubset(CONSULTING_FIRMS):

        flags.append(

            "Entire career in consulting."

        )

        multiplier *= 0.45

    # --------------------------------------------------
    # CV without NLP
    # --------------------------------------------------

    cv = skill_names & CV_SPEECH_ROBOTICS

    nlp = skill_names & NLP_IR_SIGNAL

    if cv and not nlp:

        flags.append(

            "Computer Vision profile."

        )

        multiplier *= 0.50

    # --------------------------------------------------
    # No Public Validation
    # --------------------------------------------------

    years = (

        candidate

        .get("profile", {})

        .get("years_of_experience", 0)

    )

    certificates = candidate.get(

        "certifications",

        []

    )

    if (

        years >= 5

        and

        github <= 0

        and

        len(certificates) == 0

    ):

        flags.append(

            "No GitHub or certifications."

        )

        multiplier *= 0.80

    return max(0.0, min(1.0, multiplier)), flags
