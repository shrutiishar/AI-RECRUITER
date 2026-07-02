"""
Location taxonomy used by recruiter scoring.
"""

# ==========================================================
# Tier-1 Indian Cities
# ==========================================================

TIER1_INDIAN_CITIES = {

    "bangalore",
    "bengaluru",
    "hyderabad",
    "pune",
    "mumbai",
    "delhi",
    "new delhi",
    "gurgaon",
    "gurugram",
    "noida",
    "chennai",
    "kolkata",
    "ahmedabad",

}

# ==========================================================
# Tier-2 Indian Cities
# ==========================================================

TIER2_INDIAN_CITIES = {

    "jaipur",
    "lucknow",
    "kanpur",
    "bhopal",
    "indore",
    "nagpur",
    "surat",
    "vadodara",
    "coimbatore",
    "kochi",
    "vizag",
    "visakhapatnam",
    "trivandrum",
    "mysore",
    "nashik",
    "patna",
    "raipur",
    "ranchi",
    "bhubaneswar",
    "mangalore",
    "madurai",

}

# ==========================================================
# Major International Tech Hubs
# ==========================================================

GLOBAL_TECH_HUBS = {

    "san francisco",
    "new york",
    "seattle",
    "austin",
    "boston",
    "london",
    "berlin",
    "amsterdam",
    "paris",
    "dublin",
    "singapore",
    "tokyo",
    "sydney",
    "toronto",
    "vancouver",
    "dubai",
    "zurich",

}

# ==========================================================
# Preferred Countries
# ==========================================================

PREFERRED_COUNTRIES = {

    "india",
    "united states",
    "usa",
    "canada",
    "united kingdom",
    "uk",
    "germany",
    "netherlands",
    "singapore",
    "australia",

}

# ==========================================================
# Country Normalization
# ==========================================================

COUNTRY_ALIAS = {

    "us": "usa",
    "u.s.": "usa",
    "united states of america": "usa",

    "uk": "united kingdom",
    "u.k.": "united kingdom",

    "bharat": "india",

}

# ==========================================================
# Default Welcome Cities
# ==========================================================

WELCOME_CITIES = (

    TIER1_INDIAN_CITIES

    |

    {

        "remote",

        "work from home",

        "hybrid",

    }

)
