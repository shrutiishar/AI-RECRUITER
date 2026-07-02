from datetime import date

from .helpers import parse_date

TODAY = date.today()


def behavioral_fit_score(candidate):
    """
    Behavioral signals.

    Returns
    -------
    score
    flags
    """

    flags = []

    score = 0.50

    signal = candidate.get(
        "redrob_signals",
        {}
    )

    # --------------------------------

    last_active = parse_date(

        signal.get("last_active_date")

    )

    if last_active:

        inactive = (

            TODAY -

            last_active

        ).days

        if inactive <= 30:

            score += 0.20

        elif inactive <= 90:

            score += 0.05

        elif inactive <= 180:

            score -= 0.10

            flags.append(

                "Inactive for several months."

            )

        else:

            score -= 0.30

            flags.append(

                "Inactive for a long period."

            )

    # --------------------------------

    if not signal.get(

        "open_to_work_flag",

        False

    ):

        score -= 0.15

        flags.append(

            "Not open to work."

        )

    # --------------------------------

    recruiter_response = signal.get(

        "recruiter_response_rate"

    )

    if recruiter_response is not None:

        if recruiter_response >= 0.50:

            score += 0.10

        elif recruiter_response < 0.15:

            score -= 0.20

            flags.append(

                "Poor recruiter response."

            )

    # --------------------------------

    completion = signal.get(

        "interview_completion_rate"

    )

    if completion is not None:

        if completion < 0.30:

            score -= 0.10

            flags.append(

                "Low interview completion."

            )

    score = max(0.0, min(score, 1.0))

    return score, flags
