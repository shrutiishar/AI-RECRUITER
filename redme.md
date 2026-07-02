# AI Recruiter

An AI-powered candidate ranking system that combines semantic retrieval, LLM-based job understanding, and recruiter-inspired scoring to recommend the best candidates.

---

## Features

- Semantic candidate retrieval using Sentence Transformers
- FAISS vector search
- GPT-powered job description parsing
- Hybrid ranking (semantic + recruiter scoring)
- Candidate consistency checks
- Career trajectory analysis
- Behavioral signal scoring
- Production-ready modular architecture

---

## Project Structure

```
AI-Recruiter/

├── data/
├── output/
├── parser/
├── embeddings/
├── scoring/
├── taxonomy/
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone <repository>

cd AI-Recruiter

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
OPENAI_API_KEY=your_openai_api_key
```

---

## Input Files

Place these inside `data/`

```
candidates.jsonl

job_description.docx

candidate_schema.json

sample_submission.csv
```

---

## Run

```
python main.py
```

---

## Output

Generated automatically inside `output/`

```
faiss.index

candidate_ids.pkl

submission.csv
```

---

## Pipeline

```
Job Description

↓

GPT Parsing

↓

Embedding

↓

FAISS Search

↓

Top 100 Candidates

↓

Recruiter Scoring

↓

Hybrid Ranking

↓

Final Top 10
```

---

## Technologies

- Python
- OpenAI GPT
- Sentence Transformers
- FAISS
- Pandas
- NumPy
- PyTorch
- scikit-learn
