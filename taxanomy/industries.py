"""
Industry taxonomy used for candidate trajectory
and domain relevance scoring.
"""

# ==========================================================
# Artificial Intelligence
# ==========================================================

AI_INDUSTRIES = {

    "Artificial Intelligence",
    "Machine Learning",
    "Generative AI",
    "Computer Vision",
    "Natural Language Processing",
    "Deep Learning",
    "Conversational AI",
    "Recommendation Systems",
    "Search",
    "Information Retrieval",

}

# ==========================================================
# SaaS
# ==========================================================

SAAS_INDUSTRIES = {

    "Software",
    "SaaS",
    "Cloud Software",
    "Enterprise Software",
    "Developer Tools",
    "Productivity Software",

}

# ==========================================================
# FinTech
# ==========================================================

FINTECH_INDUSTRIES = {

    "FinTech",
    "Banking",
    "Payments",
    "Insurance",
    "Trading",
    "Investment",
    "Digital Wallets",

}

# ==========================================================
# E-Commerce
# ==========================================================

ECOMMERCE_INDUSTRIES = {

    "E-Commerce",
    "Marketplace",
    "Retail",
    "Online Shopping",
    "Quick Commerce",

}

# ==========================================================
# Healthcare
# ==========================================================

HEALTHCARE_INDUSTRIES = {

    "Healthcare",
    "HealthTech",
    "Medical Devices",
    "Pharmaceuticals",
    "Biotechnology",

}

# ==========================================================
# Telecom
# ==========================================================

TELECOM_INDUSTRIES = {

    "Telecommunications",
    "Networking",
    "5G",
    "Wireless",

}

# ==========================================================
# Manufacturing
# ==========================================================

MANUFACTURING_INDUSTRIES = {

    "Manufacturing",
    "Industrial Automation",
    "Automotive",
    "Robotics",

}

# ==========================================================
# Education
# ==========================================================

EDTECH_INDUSTRIES = {

    "Education",
    "EdTech",
    "E-Learning",
    "Learning Platforms",

}

# ==========================================================
# Gaming
# ==========================================================

GAMING_INDUSTRIES = {

    "Gaming",
    "Game Development",
    "Esports",

}

# ==========================================================
# Consulting
# ==========================================================

CONSULTING_INDUSTRIES = {

    "IT Services",
    "Consulting",
    "Technology Consulting",
    "Business Consulting",

}

# ==========================================================
# Industry Weights
# ==========================================================

INDUSTRY_WEIGHTS = {

    "Artificial Intelligence": 1.00,
    "Machine Learning": 1.00,
    "Generative AI": 1.00,

    "Software": 0.95,
    "SaaS": 0.95,

    "Cloud Software": 0.90,
    "Developer Tools": 0.90,

    "FinTech": 0.85,
    "E-Commerce": 0.85,

    "Healthcare": 0.75,
    "Telecommunications": 0.70,

    "Manufacturing": 0.65,

    "Education": 0.60,

    "Gaming": 0.70,

    "Consulting": 0.55,

}

# ==========================================================
# Combined Set
# ==========================================================

ALL_INDUSTRIES = (

    AI_INDUSTRIES

    |

    SAAS_INDUSTRIES

    |

    FINTECH_INDUSTRIES

    |

    ECOMMERCE_INDUSTRIES

    |

    HEALTHCARE_INDUSTRIES

    |

    TELECOM_INDUSTRIES

    |

    MANUFACTURING_INDUSTRIES

    |

    EDTECH_INDUSTRIES

    |

    GAMING_INDUSTRIES

    |

    CONSULTING_INDUSTRIES

)
