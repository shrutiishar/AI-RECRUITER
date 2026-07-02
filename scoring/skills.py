from .helpers import (
    skill_map,
    cluster_strength,
    full_text_blob,
)


def skills_fit_score(candidate, jd):
    """
    Calculates recruiter-style skill fit.

    Returns
    -------
    score : float
    detail : dict
    """

    skills = skill_map(candidate)

    text = full_text_blob(candidate)

    detail = {}

    must_scores = []

    # ----------------------------------------
    # Must Have Skills
    # ----------------------------------------

    for label, cluster in jd.must_have_clusters.items():

        score, hits = cluster_strength(

            skills,

            cluster

        )

        detail[label] = {

            "score": score,

            "matched_skills": [

                skill["name"]

                for skill in hits

            ]

        }

        must_scores.append(score)

    # ----------------------------------------
    # Evaluation / Ranking Signals
    # ----------------------------------------

    evaluation_match = any(

        keyword.lower() in text

        for keyword in jd.eval_keywords

    )

    ranking_keywords = {

        "Ranking Systems",

        "Learning to Rank",

        "Recommendation Systems"

    }

    ranking_match = bool(

        set(skills.keys()) & ranking_keywords

    )

    if evaluation_match:

        evaluation_score = 1.0

    elif ranking_match:

        evaluation_score = 0.50

    else:

        evaluation_score = 0.0

    detail["evaluation"] = {

        "score": evaluation_score,

        "matched_skills": [

            "text evidence"

        ] if evaluation_match else []

    }

    must_scores.append(evaluation_score)

    # ----------------------------------------
    # Nice To Have
    # ----------------------------------------

    nice_scores = []

    for label, cluster in jd.nice_to_have_clusters.items():

        score, hits = cluster_strength(

            skills,

            cluster

        )

        detail[label] = {

            "score": score,

            "matched_skills": [

                skill["name"]

                for skill in hits

            ]

        }

        nice_scores.append(score)

    # ----------------------------------------
    # Final Score
    # ----------------------------------------

    must_average = (

        sum(must_scores)

        /

        max(len(must_scores), 1)

    )

    if len(nice_scores):

        nice_average = (

            sum(nice_scores)

            /

            len(nice_scores)

        )

    else:

        nice_average = 0

    final_score = (

        0.80 * must_average

        +

        0.20 * nice_average

    )

    return final_score, detail
