"""
Global constants used throughout the recruiter engine.
"""

# ==========================================================
# Experience Buckets
# ==========================================================

FRESHER_MAX = 1

JUNIOR_MIN = 1
JUNIOR_MAX = 3

MID_MIN = 3
MID_MAX = 6

SENIOR_MIN = 6
SENIOR_MAX = 10

STAFF_MIN = 10

# ==========================================================
# Notice Period Thresholds
# ==========================================================

IDEAL_NOTICE_DAYS = 30

GOOD_NOTICE_DAYS = 45

ACCEPTABLE_NOTICE_DAYS = 60

LONG_NOTICE_DAYS = 90

# ==========================================================
# Skill Proficiency Mapping
# ==========================================================

PROFICIENCY_SCORE = {

    "beginner": 0.25,

    "intermediate": 0.55,

    "advanced": 0.80,

    "expert": 1.00,

}

# ==========================================================
# Recruiter Score Weights
# ==========================================================

DEFAULT_SCORE_WEIGHTS = {

    "skills": 0.38,

    "trajectory": 0.22,

    "experience": 0.12,

    "location": 0.12,

    "behavioral": 0.10,

    "logistics": 0.06,

}

# ==========================================================
# Penalty Multipliers
# ==========================================================

MAX_PENALTY = 0.05

MIN_MULTIPLIER = 0.20

DEFAULT_MULTIPLIER = 1.00

# ==========================================================
# Candidate Activity
# ==========================================================

ACTIVE_WITHIN_DAYS = 30

MODERATE_ACTIVITY_DAYS = 90

STALE_ACTIVITY_DAYS = 180

# ==========================================================
# GitHub Activity
# ==========================================================

GOOD_GITHUB_SCORE = 70

AVERAGE_GITHUB_SCORE = 40

LOW_GITHUB_SCORE = 20

# ==========================================================
# Recruiter Behaviour
# ==========================================================

GOOD_RESPONSE_RATE = 0.60

AVERAGE_RESPONSE_RATE = 0.30

LOW_RESPONSE_RATE = 0.10

# ==========================================================
# Interview Completion
# ==========================================================

GOOD_COMPLETION = 0.80

AVERAGE_COMPLETION = 0.50

LOW_COMPLETION = 0.25

# ==========================================================
# Retrieval
# ==========================================================

TOP_K_VECTOR_SEARCH = 100

TOP_K_RERANK = 25

FINAL_SHORTLIST = 10

# ==========================================================
# Embedding Models
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

RERANKER_MODEL = "BAAI/bge-reranker-large"

# ==========================================================
# OpenAI
# ==========================================================

LLM_MODEL = "gpt-4.1"

LLM_TEMPERATURE = 0.0

# ==========================================================
# Output
# ==========================================================

CSV_FILENAME = "submission.csv"

EXPLANATION_WORD_LIMIT = 80

# ==========================================================
# Resume Parsing
# ==========================================================

MAX_RESUME_LENGTH = 12000

MAX_JD_LENGTH = 8000
