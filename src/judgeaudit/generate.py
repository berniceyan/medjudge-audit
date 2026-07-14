import json
from pathlib import Path
from judgeaudit.llm import chat
from judgeaudit.data import DATA_DIR

RESPONSE_MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-sonnet-4.5",
]

def generate_responses(sample_file: str = "sample_400.jsonl", limit: int | None = None):
    examples = [json.loads(l) for l in open(DATA_DIR / sample_file)]
    if limit:
        examples = examples[:limit] # pilot mode
    out = Path("results/responses.jsonl")
    out.parent.mkdir(exist_ok=True)
    with open(out, "w") as f:
        for i, e in enumerate(examples):
            for model in RESPONSE_MODELS:
                text = chat(model, e["prompt"], temperature=1.0)
                f.write(json.dumps({"prompt_id": e["prompt_id"],
                                    "model": model, "response": text}) + "\n")
            print(f"{i+1}/{len(examples)}")