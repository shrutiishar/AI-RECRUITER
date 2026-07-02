import json

from embeddings.embedder import CandidateEmbedder
from embeddings.vector_store import VectorStore

from scoring.scorer import score_candidate

import config


class SemanticRetriever:

    def __init__(self):

        self.embedder = CandidateEmbedder()

        self.vector_db = VectorStore()

        self.vector_db.load()

    # --------------------------------------------------------

    def load_candidates(self):

        candidates = []

        with open(

            config.CANDIDATE_FILE,

            "r",

            encoding="utf-8"

        ) as f:

            for line in f:

                candidates.append(

                    json.loads(line)

                )

        return candidates

    # --------------------------------------------------------

    def candidate_lookup(self, candidates):

        lookup = {}

        for candidate in candidates:

            cid = candidate.get(

                "candidate_id",

                candidate.get("id")

            )

            lookup[cid] = candidate

        return lookup

    # --------------------------------------------------------

    def retrieve(

        self,

        jd,

        top_k=100

    ):

        query_vector = self.embedder.embed_job_description(

            jd

        )

        semantic_hits = self.vector_db.search(

            query_vector,

            top_k

        )

        candidates = self.load_candidates()

        lookup = self.candidate_lookup(

            candidates

        )

        results = []

        for hit in semantic_hits:

            cid = hit["candidate_id"]

            if cid not in lookup:

                continue

            candidate = lookup[cid]

            recruiter_score = score_candidate(

                candidate,

                jd

            )

            recruiter_score["candidate_id"] = cid

            recruiter_score["semantic_score"] = hit["semantic_score"]

            # ----------------------------------------
            # Hybrid Score
            # ----------------------------------------

            recruiter_score["final_score"] = (

                0.40

                *

                hit["semantic_score"]

                +

                0.60

                *

                recruiter_score["score"]

            )

            results.append(

                recruiter_score

            )

        results.sort(

            key=lambda x: x["final_score"],

            reverse=True

        )

        return results

    # --------------------------------------------------------

    def top_candidates(

        self,

        jd,

        top_n=10

    ):

        ranked = self.retrieve(

            jd,

            config.TOP_K_RETRIEVAL

        )

        return ranked[:top_n]
