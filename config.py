import os

# ==========================================================
# API Keys
# ==========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==========================================================
# Data Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ==========================================================
# Input Files
# ==========================================================

CANDIDATE_FILE = os.path.join(
    DATA_DIR,
    "candidates.jsonl"
)

JD_FILE = os.path.join(
    DATA_DIR,
    "job_description.docx"
)

SCHEMA_FILE = os.path.join(
    DATA_DIR,
    "candidate_schema.json"
)

SAMPLE_SUBMISSION = os.path.join(
    DATA_DIR,
    "sample_submission.csv"
)

# ==========================================================
# FAISS
# ==========================================================

VECTOR_INDEX = os.path.join(
    OUTPUT_DIR,
    "faiss.index"
)

EMBEDDINGS_FILE = os.path.join(
    OUTPUT_DIR,
    "candidate_ids.pkl"
)

# ==========================================================
# Models
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

OPENAI_MODEL = "gpt-4.1"

# ==========================================================
# Retrieval
# ==========================================================

TOP_K_RETRIEVAL = 100

FINAL_TOP_K = 10

# ==========================================================
# Output
# ==========================================================

CSV_FILENAME = "submission.csv"
