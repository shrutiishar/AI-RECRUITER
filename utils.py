import json
import pickle
import os


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_jsonl(path):

    rows = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:
            rows.append(json.loads(line))

    return rows


def save_pickle(obj, path):

    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):

    with open(path, "rb") as f:
        return pickle.load(f)


def ensure_directory(path):

    os.makedirs(path, exist_ok=True)


def normalize_text(text):

    if text is None:
        return ""

    return " ".join(

        str(text)

        .lower()

        .strip()

        .split()

    )
