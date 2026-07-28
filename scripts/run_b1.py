# scripts/run_b1.py — Track B run 1: gpt-4.1 judge × v1 variant × (402 examples × 2 models × ~10 criteria)
import json
import time
from pathlib import Path
from judgeaudit.data import DATA_DIR
from judgeaudit.judge import grade_one

OUT = Path("results/grades_track_b1.jsonl")
OUT.parent.mkdir(exist_ok=True)

JUDGE = "openai/gpt-4.1"

def conv_text(messages):
    return "\n\n".join(f"{m['role']}: {m['content']}" for m in messages)

def theme_of(e):
    t = [x for x in e["example_tags"] if x.startswith("theme:")]
    return t[0] if t else "theme:unknown"

def main(limit: int | None = None):
    start = time.time()
    examples = {e["prompt_id"]: e for e in
                (json.loads(l) for l in open(DATA_DIR / "sample_400.jsonl"))}
    responses = [json.loads(l) for l in open("results/responses.jsonl")]

    if limit:
        keep = set(list(examples)[:limit])
        responses = [r for r in responses if r["prompt_id"] in keep]

    done = set()
    if OUT.exists():
        for line in open(OUT):
            r = json.loads(line)
            done.add((r["prompt_id"], r["response_model"], r["criterion_idx"]))

    with open(OUT, "a") as f:
        for i, r in enumerate(responses):
            e = examples[r["prompt_id"]]
            convo = conv_text(e["prompt"])
            n_crit = len(e["rubrics"])
            for ci, rub in enumerate(e["rubrics"]):
                if (r["prompt_id"], r["model"], ci) in done:
                    continue
                print(f" response {i+1}/{len(responses)} criterion {ci+1}/{n_crit}", end="\r", flush=True) # in-place ticker: one tick per API call
                grade = grade_one(JUDGE, "v1_official", convo, r["response"], rub["criterion"])
                f.write(json.dumps({
                    "prompt_id": r["prompt_id"], "response_model": r["model"],
                    "judge_model": JUDGE, "variant": "v1_official", "run_tag": "",
                    "criterion_idx": ci, "points": rub["points"],
                    "grade": grade, "theme": theme_of(e),
                }) + "\n")
            rate = (time.time() - start) / (i + 1)
            left = rate * (len(responses) - i - 1) / 3600 
            print(f"{i+1}/{len(responses)} responses done ~{left:.1f}h left ", flush=True)

if __name__ == "__main__":
    main()