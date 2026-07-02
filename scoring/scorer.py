from .consistency import consistency_check
from .disqualifiers import disqualifier_check
from .preferences import do_not_want_check

from .skills import skills_fit_score
from .trajectory import trajectory_fit_score
from .experience import experience_fit_score
from .location import location_fit_score
from .logistics import logistics_fit_score
from .behavioral import behavioral_fit_score


# -------------------------------------------------------
# Default Recruiter Weights
# -------------------------------------------------------

WEIGHTS = {

    "skills": 0.38,

    "trajectory": 0.22,

    "experience": 0.12,

    "location": 0.12,

    "logistics": 0.06,

    "behavioral": 0.10

}


# -------------------------------------------------------
# Main Candidate Scoring Function
# -------------------------------------------------------

def score_candidate(candidate, jd):
    """
    Master scoring function.

    Returns
    -------
    dict
    """

    # --------------------------------------------
    # Multipliers
    # --------------------------------------------

    consistency_multiplier, consistency_flags = (

        consistency_check(candidate)

    )

    disqualifier_multiplier, disqualifier_flags = (

        disqualifier_check(candidate)

    )

    preference_multiplier, preference_flags = (

        do_not_want_check(candidate)

    )

    # --------------------------------------------
    # Positive Scores
    # --------------------------------------------

    skill_score, skill_details = (

        skills_fit_score(candidate, jd)

    )

    trajectory_score, trajectory_flags = (

        trajectory_fit_score(candidate)

    )

    experience_score = (

        experience_fit_score(candidate, jd)

    )

    location_score, location_flags = (

        location_fit_score(candidate, jd)

    )

    logistics_score, logistics_flags = (

        logistics_fit_score(candidate, jd)

    )

    behavioral_score, behavioral_flags = (

        behavioral_fit_score(candidate)

    )

    # --------------------------------------------
    # Weighted Base Score
    # --------------------------------------------

    base_score = (

        WEIGHTS["skills"] * skill_score

        +

        WEIGHTS["trajectory"] * trajectory_score

        +

        WEIGHTS["experience"] * experience_score

        +

        WEIGHTS["location"] * location_score

        +

        WEIGHTS["logistics"] * logistics_score

        +

        WEIGHTS["behavioral"] * behavioral_score

    )

    # --------------------------------------------
    # Apply Penalties
    # --------------------------------------------

    multiplier = (

        consistency_multiplier

        *

        disqualifier_multiplier

        *

        preference_multiplier

    )

    final_score = base_score * multiplier

    final_score = max(

        0.0,

        min(final_score, 1.0)

    )

    # --------------------------------------------
    # Return Everything
    # --------------------------------------------

    return {

        "score": final_score,

        "base_score": base_score,

        "multiplier": multiplier,

        "sub_scores": {

            "skills": skill_score,

            "trajectory": trajectory_score,

            "experience": experience_score,

            "location": location_score,

            "logistics": logistics_score,

            "behavioral": behavioral_score

        },

        "skills_detail": skill_details,

        "flags": {

            "consistency": consistency_flags,

            "disqualifiers": disqualifier_flags,

            "preferences": preference_flags,

            "trajectory": trajectory_flags,

            "location": location_flags,

            "logistics": logistics_flags,

            "behavioral": behavioral_flags

        }

    }


# -------------------------------------------------------
# Batch Scoring
# -------------------------------------------------------

def score_all_candidates(candidates, jd):
    """
    Scores every candidate and returns them ranked.
    """

    results = []

    for candidate in candidates:

        result = score_candidate(candidate, jd)

        result["candidate_id"] = candidate.get(
            "candidate_id",
            candidate.get("id")
        )

        results.append(result)

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return results
