from .helpers import full_text_blob, skill_map

from taxonomy import (
    EMBEDDINGS_RETRIEVAL,
    VECTOR_DB_HYBRID_SEARCH,
    FRAMEWORK_WRAPPER_SKILLS,
    PRE_LLM_ERA_SIGNAL,
    NON_CODING_SENIOR_TITLES,
)


def disqualifier_check(candidate):
    """
    Checks strong negative signals.

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

    text = full_text_blob(candidate)

    # ---------------------------------------------------
    # Research only profile
    # ---------------------------------------------------

    research_signals = [

        "research scientist",
        "research intern",
        "academic lab",
        "research fellow",
        "phd",
        "postdoctoral"

    ]

    production_signals = [

        "production",
        "deployed",
        "live traffic",
        "real users",
        "scale",
        "shipped"

    ]

    research = any(

        word in text

        for word in research_signals

    )

    production = any(

        word in text

        for word in production_signals

    )

    if research and not production:

        flags.append(

            "Research profile without production deployment."

        )

        multiplier *= 0.05

    # ---------------------------------------------------
    # Wrapper AI only
    # ---------------------------------------------------

    ai_skills = (

        EMBEDDINGS_RETRIEVAL

        |

        VECTOR_DB_HYBRID_SEARCH

        |

        FRAMEWORK_WRAPPER_SKILLS

        |

        {"LLMs"}

    )

    present = skill_names & ai_skills

    only_wrapper = (

        len(present) > 0

        and

        present.issubset(

            FRAMEWORK_WRAPPER_SKILLS

            |

            {"LLMs"}

        )

    )

    shallow = True

    for skill in present:

        if skills[skill].get("duration_months", 0) >= 12:

            shallow = False

    pre_llm = len(

        skill_names

        &

        PRE_LLM_ERA_SIGNAL

    ) > 0

    if only_wrapper and shallow and not pre_llm:

        flags.append(

            "Recent LLM framework experience only."

        )

        multiplier *= 0.30

    # ---------------------------------------------------
    # Non coding manager
    # ---------------------------------------------------

    current_title = (

        candidate

        .get("profile", {})

        .get("current_title", "")

        .lower()

    )

    current_job = None

    for job in career:

        if job.get("is_current"):

            current_job = job

            break

    if current_job:

        if any(

            title in current_title

            for title in NON_CODING_SENIOR_TITLES

        ):

            months = current_job.get(

                "duration_months",

                0

            )

            if months >= 18:

                flags.append(

                    "Long-term non-coding leadership role."

                )

                multiplier *= 0.35

    # ---------------------------------------------------
    # No Python
    # ---------------------------------------------------

    if "Python" not in skill_names:

        flags.append(

            "Python skill missing."

        )

        multiplier *= 0.50

    # ---------------------------------------------------
    # No ML experience
    # ---------------------------------------------------

    ml_keywords = [

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "retrieval",
        "ranking",
        "nlp"

    ]

    if not any(

        word in text

        for word in ml_keywords

    ):

        flags.append(

            "No production ML evidence."

        )

        multiplier *= 0.60

    return max(0.0, min(1.0, multiplier)), flags
