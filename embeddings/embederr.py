from sentence_transformers import SentenceTransformer
import numpy as np
import json
from tqdm import tqdm

import config


class CandidateEmbedder:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            config.EMBEDDING_MODEL
        )

    # -----------------------------------------------------

    def candidate_to_text(self, candidate):

        profile = candidate.get("profile", {})

        text = []

        text.append(profile.get("headline", ""))

        text.append(profile.get("summary", ""))

        text.append(profile.get("current_title", ""))

        text.append(profile.get("current_company", ""))

        # -------------------------
        # Skills
        # -------------------------

        skills = candidate.get("skills", [])

        skill_text = []

        for skill in skills:

            name = skill.get("name", "")

            prof = skill.get("proficiency", "")

            duration = skill.get(
                "duration_months",
                0
            )

            skill_text.append(

                f"{name} {prof} {duration} months"

            )

        text.append(" ".join(skill_text))

        # -------------------------
        # Career
        # -------------------------

        career = candidate.get(
            "career_history",
            []
        )

        for job in career:

            text.append(

                job.get("title", "")

            )

            text.append(

                job.get("company", "")

            )

            text.append(

                job.get("description", "")

            )

        return "\n".join(text)

    # -----------------------------------------------------

    def embed_candidate(self, candidate):

        text = self.candidate_to_text(candidate)

        embedding = self.model.encode(

            text,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        return embedding

    # -----------------------------------------------------

    def embed_job_description(self, jd):

        embedding = self.model.encode(

            jd.raw_text,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        return embedding

    # -----------------------------------------------------

    def build_embeddings(self, candidates):

        vectors = []

        ids = []

        print(

            f"Embedding {len(candidates)} candidates..."

        )

        for candidate in tqdm(candidates):

            vector = self.embed_candidate(candidate)

            vectors.append(vector)

            ids.append(

                candidate.get(

                    "candidate_id",

                    candidate.get("id")

                )

            )

        vectors = np.array(

            vectors,

            dtype=np.float32

        )

        return ids, vectors


# ---------------------------------------------------------

def load_candidates(path):

    candidates = []

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        for line in f:

            candidates.append(

                json.loads(line)

            )

    return candidates


# ---------------------------------------------------------

if __name__ == "__main__":

    embedder = CandidateEmbedder()

    candidates = load_candidates(

        config.CANDIDATE_FILE

    )

    ids, vectors = embedder.build_embeddings(

        candidates

    )

    print(vectors.shape)
