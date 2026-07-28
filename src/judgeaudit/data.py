import json, urllib.request
from pathlib import Path
import random 

DATA_DIR = Path("data")

# 2026-07-10
# most updated URLs for main, hard, consensus from 
# https://github.com/openai/simple-evals/blob/main/healthbench_eval.py
URLS = {
    "main": "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/2025-05-07-06-14-12_oss_eval.jsonl",
    "hard": "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/hard_2025-05-08-21-00-10.jsonl",
    "consensus": "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/consensus_2025-05-09-20-00-46.jsonl",

    # Track A ground truth from https://github.com/openai/simple-evals/blob/main/healthbench_meta_eval.py
    "meta_eval": "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/2025-05-07-06-14-12_oss_meta_eval.jsonl",
}

def download_all():
    DATA_DIR.mkdir(exist_ok=True)
    for name, url in URLS.items():
        dest = DATA_DIR / f"{name}.jsonl"
        if not dest.exists():
            print(f"downloading {name}...")
            urllib.request.urlretrieve(url, dest)

def load_examples(name: str = "main") -> list[dict]:
    with open(DATA_DIR / f"{name}.jsonl") as f:
        return [json.loads(line) for line in f]

def theme_of(example: dict) -> str:
    themes = [t for t in example["example_tags"]]
    return themes[0] if themes else "theme:unknown"

def stratified_sample(examples: list[dict], n: int, seed: int = 0) -> list[dict]:
    """Sample n examples, preserving theme proportions."""
    rng = random.Random(seed)
    by_theme: dict[str, list] = {}

    for e in examples:
        by_theme.setdefault(theme_of(e), []).append(e)

    total = len(examples)
    sample = []

    for theme, group in sorted(by_theme.items()):
        k = round(n * len(group) / total)
        sample.extend(rng.sample(group, min(k, len(group))))

    return sample

def save_sample(n: int = 400):
    sample = stratified_sample(load_examples("main"), n)
    with open(DATA_DIR / f"sample_{n}.jsonl", "w") as f:
        for e in sample:
            f.write(json.dumps(e) + "\n")