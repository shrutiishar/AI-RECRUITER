from .helpers import candidate_skill_proficiency


def consistency_check(candidate):
    """
    Detects suspicious or internally inconsistent candidate profiles.

    Returns:
        multiplier : float
        flags : list[str]
    """

    flags = []
    multiplier = 1.0

    profile = candidate.get("profile", {})
    career = candidate.get("career_history", [])
    skills = candidate.get("skills", [])

    years = profile.get("years_of_experience", 0) or 0

    total_months = sum(
        job.get("duration_months", 0)
        for job in career
    )

    # -------------------------------------------------
    # Experience mismatch
    # -------------------------------------------------

    if years >= 2 and total_months > 0:

        ratio = total_months / (years * 12)

        if ratio < 0.40:

            flags.append(
                f"Career history covers only {total_months} months "
                f"while profile claims {years:.1f} years experience."
            )

            multiplier *= 0.35

        elif ratio > 1.60:

            flags.append(
                f"Career duration exceeds claimed experience."
            )

            multiplier *= 0.60

    # -------------------------------------------------
    # Expert with zero experience
    # -------------------------------------------------

    fake_experts = []

    for skill in skills:

        if (
            skill.get("proficiency") == "expert"
            and skill.get("duration_months", 0) == 0
        ):

            fake_experts.append(skill["name"])

    if fake_experts:

        flags.append(

            "Expert proficiency with zero duration: "

            + ", ".join(fake_experts)

        )

        multiplier *= max(

            0.25,

            1 - 0.20 * len(fake_experts)

        )

    # -------------------------------------------------
    # Single job longer than total experience
    # -------------------------------------------------

    for job in career:

        months = job.get("duration_months", 0)

        if months > years * 12 + 3:

            flags.append(

                f"{job.get('company')} duration "

                f"({months} months) exceeds "

                f"claimed total experience."

            )

            multiplier *= 0.40

            break

    # -------------------------------------------------
    # Skill assessment contradiction
    # -------------------------------------------------

    assessment_scores = (

        candidate

        .get("redrob_signals", {})

        .get("skill_assessment_scores", {})

    )

    contradictions = []

    for skill, score in assessment_scores.items():

        if (

            score is not None

            and score < 15

            and candidate_skill_proficiency(
                candidate,
                skill
            ) in ("advanced", "expert")

        ):

            contradictions.append(skill)

    if contradictions:

        flags.append(

            "Assessment contradicts claimed expertise: "

            + ", ".join(contradictions)

        )

        multiplier *= max(

            0.50,

            1 - 0.15 * len(contradictions)

        )

    # -------------------------------------------------
    # Extremely high number of skills
    # -------------------------------------------------

    if len(skills) > 80:

        flags.append(

            "Unusually high number of listed skills."

        )

        multiplier *= 0.90

    # -------------------------------------------------
    # Duplicate skill detection
    # -------------------------------------------------

    names = [s["name"] for s in skills]

    if len(names) != len(set(names)):

        flags.append(

            "Duplicate skills detected."

        )

        multiplier *= 0.95

    return max(0.0, min(1.0, multiplier)), flags
