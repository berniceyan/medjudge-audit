# scripts/run_b3.py — 5 reps @ temp 1.0, gpt-4.1 × v1, first 26 examples (~500 pairs)
import json
import time
from pathlib import Path
from judgeaudit.data import DATA_DIR
from judgeaudit.judge import grade_one

OUT = Path("results/grades_track_b3.jsonl") 
OUT.parent.mkdir(exist_ok=True)
JUDGE, N_EX, N_REPS = "openai/gpt-4.1", 26, 5

def conv_text(m):
    return "\n\n".join(f"{x['role']}: {x['content']}" for x in m)

def main():
    start = time.time()
    examples = {e["prompt_id"]: e for e in (json.loads(l) for l in open(DATA_DIR / "sample_400.jsonl"))} 
    keep = set(list(examples)[:N_EX])
    responses = [r for r in (json.loads(l) for l in open("results/responses.jsonl")) if r["prompt_id"] in keep]

    done = set()
    if OUT.exists():
        done = {(x["prompt_id"], x["response_model"], x["criterion_idx"], x["run_tag"]) for x in (json.loads(l) for l in open(OUT))}
    
    with open(OUT, "a") as f:
        for i, r in enumerate(responses):
            e = examples[r["prompt_id"]]
            convo = conv_text(e["prompt"])
            for ci, rub in enumerate(e["rubrics"]):
                for rep in range(N_REPS):
                    tag = f"rep{rep}"
                    if (r["prompt_id"], r["model"], ci, tag) in done:
                        continue
                    print(f" resp {i+1}/{len(responses)} crit {ci+1} {tag}", end="\r", flush=True)
                    g = grade_one(JUDGE, "v1_official", convo, r["response"], rub["criterion"], run_tag=tag, temperature=1.0)
                    f.write(json.dumps({
                        "prompt_id": r["prompt_id"], "response_model": r["model"], "judge_model": JUDGE, 
                        "variant": "v1_official", "run_tag": tag, "criterion_idx": ci, "points": rub["points"], "grade": g}) + "\n")
            rate = (time.time() - start) / (i + 1)
            print(f"{i+1}/{len(responses)} ~{rate*(len(responses)-i-1)/3600:.1f}h left ", flush=True) # trailing spaces wipe the ticker line

if __name__ == "__main__":
    main()