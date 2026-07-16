# cells: gpt-4.1 × {v2,v3} + flash × {v1,v2,v3} (gpt-4.1 × v1 reused from B1 run)
import json
import time
from pathlib import Path
from judgeaudit.data import DATA_DIR
from judgeaudit.judge import grade_one

OUT = Path("results/grades_track_b2.jsonl") 
OUT.parent.mkdir(exist_ok=True)

CELLS = [("openai/gpt-4.1", "v2_terse"),
         ("openai/gpt-4.1", "v3_clinical_persona"), 
         ("google/gemini-2.5-flash", "v1_official"), 
         ("google/gemini-2.5-flash", "v2_terse"), 
         ("google/gemini-2.5-flash", "v3_clinical_persona")]

N_EX = 100

def conv_text(m):
    return "\n\n".join(f"{x['role']}: {x['content']}" for x in m)

def main():
    start = time.time()
    examples = {e["prompt_id"]: e for e in (json.loads(l) for l in open(DATA_DIR / "sample_400.jsonl"))} 
    keep = set(list(examples)[:N_EX])
    responses = [r for r in (json.loads(l) for l in open("results/responses.jsonl")) if r["prompt_id"] in keep]
    done = set()
    if OUT.exists():
        done = {(x["prompt_id"], x["response_model"], x["criterion_idx"], x["judge_model"], x["variant"]) 
                for x in (json.loads(l) for l in open(OUT))}
    with open(OUT, "a") as f:
        for i, r in enumerate(responses):
            e = examples[r["prompt_id"]]
            convo = conv_text(e["prompt"])
            for ci, rub in enumerate(e["rubrics"]):
                for judge, variant in CELLS:
                    if (r["prompt_id"], r["model"], ci, judge, variant) in done:
                        continue
                    print(f" resp {i+1}/{len(responses)} crit {ci+1} " f"{judge.split('/')[1]} × {variant}",
                    end="\r", flush=True)
                    g = grade_one(judge, variant, convo, r["response"], rub["criterion"])
                    f.write(json.dumps({
                        "prompt_id": r["prompt_id"], "response_model": r["model"], "judge_model": judge, "variant": variant, "run_tag": "", 
                        "criterion_idx": ci, "points": rub["points"], "grade": g}) + "\n")
            rate = (time.time() - start) / (i + 1)
            print(f"{i+1}/{len(responses)} ~{rate*(len(responses)-i-1)/3600:.1f}h left ", flush=True) # trailing spaces wipe the ticker line

if __name__ == "__main__": 
    main()