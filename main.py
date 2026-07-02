import json
import os
import pandas as pd

import config

from parser.jd_parser import parse_job_description

from embeddings.embedder import (
    CandidateEmbedder,
    load_candidates,
)

from embeddings.vector_store import (
    build_vector_database,
    VectorStore,
)

from embeddings.retriever import SemanticRetriever


# ==========================================================
# Build FAISS Index (Only Once)
# ==========================================================

def build_index():

    print("=" * 60)
    print("Building FAISS Index")
    print("=" * 60)

    embedder = CandidateEmbedder()

    candidates = load_candidates(
        config.CANDIDATE_FILE
    )

    ids, vectors = embedder.build_embeddings(
        candidates
    )

    build_vector_database(
        ids,
        vectors
    )

    print("Vector database created.\n")


# ==========================================================
# Rank Candidates
# ==========================================================

def rank_candidates():

    print("=" * 60)
    print("Parsing Job Description")
    print("=" * 60)

    jd = parse_job_description(
        config.JD_FILE
    )

    print("Job Title:", jd.title)

    print("\nSearching Candidates...\n")

    retriever = SemanticRetriever()

    ranked = retriever.top_candidates(
        jd,
        top_n=config.FINAL_TOP_K
    )

    return ranked


# ==========================================================
# Save Submission
# ==========================================================

def save_submission(results):

    rows = []

    for rank, result in enumerate(results, start=1):

        rows.append({

            "rank": rank,

            "candidate_id": result["candidate_id"],

            "score": round(
                result["final_score"],
                4
            ),

            "semantic_score": round(
                result["semantic_score"],
                4
            ),

            "recruiter_score": round(
                result["score"],
                4
            ),

            "flags": json.dumps(
                result["flags"]
            )

        })

    df = pd.DataFrame(rows)

    os.makedirs(
        config.OUTPUT_DIR,
        exist_ok=True
    )

    output_file = os.path.join(

        config.OUTPUT_DIR,

        config.CSV_FILENAME

    )

    df.to_csv(

        output_file,

        index=False

    )

    print("\nSubmission saved to:")
    print(output_file)

    return df


# ==========================================================
# Pretty Print
# ==========================================================

def show_results(results):

    print("\n")

    print("=" * 80)

    print("TOP CANDIDATES")

    print("=" * 80)

    for i, candidate in enumerate(results, start=1):

        print(f"\n#{i}")

        print(
            "Candidate ID:",
            candidate["candidate_id"]
        )

        print(
            "Final Score:",
            round(candidate["final_score"], 4)
        )

        print(
            "Semantic:",
            round(candidate["semantic_score"], 4)
        )

        print(
            "Recruiter:",
            round(candidate["score"], 4)
        )

        print("-" * 80)


# ==========================================================
# Main
# ==========================================================

def main():

    # Build embeddings once
    if not os.path.exists(config.VECTOR_INDEX):

        build_index()

    # Rank
    ranked = rank_candidates()

    # Display
    show_results(ranked)

    # Save CSV
    save_submission(ranked)


if __name__ == "__main__":

    main()
