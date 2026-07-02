from dataclasses import dataclass, field
from typing import Dict, List, Set
from docx import Document
from openai import OpenAI

import config
from taxonomy import *

client = OpenAI(api_key=config.OPENAI_API_KEY)


# =====================================================
# Structured JD Object
# =====================================================

@dataclass
class JobDescription:

    title: str = ""

    exp_min: int = 0
    exp_max: int = 20

    exp_ideal_min: int = 0
    exp_ideal_max: int = 20

    primary_cities: Set[str] = field(default_factory=set)
    welcome_cities: Set[str] = field(default_factory=set)

    max_notice_days_ideal: int = 30

    must_have_clusters: Dict[str, Set[str]] = field(default_factory=dict)
    nice_to_have_clusters: Dict[str, Set[str]] = field(default_factory=dict)

    eval_keywords: List[str] = field(default_factory=list)

    raw_text: str = ""


# =====================================================
# Read DOCX
# =====================================================

def read_job_description(path):

    doc = Document(path)

    text = []

    for para in doc.paragraphs:

        if para.text.strip():

            text.append(para.text.strip())

    return "\n".join(text)


# =====================================================
# GPT Parser
# =====================================================

def parse_with_llm(jd_text):

    prompt = f"""
You are an expert technical recruiter.

Extract the following information from the job description.

Return ONLY valid JSON.

{{
"title":"",
"experience_min":0,
"experience_max":0,
"locations":[],
"must_have_skills":[],
"nice_to_have_skills":[],
"evaluation_keywords":[]
}}

Job Description:

{jd_text}
"""

    response = client.chat.completions.create(

        model="gpt-4.1",

        messages=[

            {
                "role":"system",
                "content":"You are an expert recruiter."
            },

            {
                "role":"user",
                "content":prompt
            }

        ],

        response_format={
            "type":"json_object"
        }

    )

    return response.choices[0].message.content


# =====================================================
# Convert Skills -> Taxonomy Clusters
# =====================================================

def build_cluster_dictionary(skill_list):

    clusters = {}

    taxonomy = {

        "Python":PYTHON_SKILLS,

        "Machine Learning":ML_CORE,

        "Deep Learning":DEEP_LEARNING,

        "NLP":NLP_IR_SIGNAL,

        "Embeddings":EMBEDDINGS_RETRIEVAL,

        "Vector DB":VECTOR_DB_HYBRID_SEARCH,

        "LLMs":LLM_FRAMEWORKS,

        "MLOps":MLOPS,

        "Cloud":CLOUD,

        "Docker":DOCKER,

        "Kubernetes":KUBERNETES

    }

    for skill in skill_list:

        for label, cluster in taxonomy.items():

            if skill.lower() in {

                s.lower()

                for s in cluster

            }:

                clusters[label] = cluster

    return clusters


# =====================================================
# Public Function
# =====================================================

def parse_job_description(path):

    import json

    text = read_job_description(path)

    parsed = json.loads(

        parse_with_llm(text)

    )

    jd = JobDescription()

    jd.title = parsed.get(

        "title",

        ""

    )

    jd.exp_min = parsed.get(

        "experience_min",

        0

    )

    jd.exp_max = parsed.get(

        "experience_max",

        20

    )

    jd.exp_ideal_min = jd.exp_min

    jd.exp_ideal_max = jd.exp_max

    jd.primary_cities = {

        city.lower()

        for city in parsed.get(

            "locations",

            []

        )

    }

    jd.must_have_clusters = build_cluster_dictionary(

        parsed.get(

            "must_have_skills",

            []

        )

    )

    jd.nice_to_have_clusters = build_cluster_dictionary(

        parsed.get(

            "nice_to_have_skills",

            []

        )

    )

    jd.eval_keywords = parsed.get(

        "evaluation_keywords",

        []

    )

    jd.raw_text = text

    return jd


# =====================================================
# Debug
# =====================================================

if __name__ == "__main__":

    jd = parse_job_description(

        config.JD_FILE

    )

    print(jd)
