def logistics_fit_score(candidate, jd):
    """
    Scores notice period.

    Returns
    -------
    score
    flags
    """

    flags = []

    notice = (

        candidate

        .get("redrob_signals", {})

        .get("notice_period_days", 60)

    )

    if notice <= jd.max_notice_days_ideal:

        return 1.0, flags

    if notice <= 60:

        flags.append(

            f"{notice} day notice period."

        )

        return 0.70, flags

    flags.append(

        f"Long notice period ({notice} days)."

    )

    return 0.45, flags
