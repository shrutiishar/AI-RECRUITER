from taxonomy import (
    TIER1_INDIAN_CITIES,
)


def location_fit_score(candidate, jd):
    """
    Scores candidate location.

    Returns
    -------
    score
    flags
    """

    flags = []

    profile = candidate.get("profile", {})

    location = profile.get("location", "").lower()
    country = profile.get("country", "").lower()

    relocate = (
        candidate
        .get("redrob_signals", {})
        .get("willing_to_relocate", False)
    )

    city = location.split(",")[0].strip()

    # ------------------------------------
    # Primary Cities
    # ------------------------------------

    if city in jd.primary_cities:

        return 1.0, flags

    # ------------------------------------
    # Welcome Cities
    # ------------------------------------

    if city in jd.welcome_cities:

        return 0.85, flags

    # ------------------------------------
    # Tier-1 Cities
    # ------------------------------------

    if country == "india":

        if city in TIER1_INDIAN_CITIES:

            return 0.70, flags

        if relocate:

            flags.append(
                "Outside preferred city but willing to relocate."
            )

            return 0.55, flags

        return 0.40, flags

    # ------------------------------------
    # Outside India
    # ------------------------------------

    if relocate:

        flags.append(
            "Outside India but willing to relocate."
        )

        return 0.30, flags

    flags.append(
        "Outside India with no relocation preference."
    )

    return 0.10, flags
