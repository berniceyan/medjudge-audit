# Track A run 1: 3 judges × v1 × 2,000 meta-eval items

import hashlib, json, random
from pathlib import Path
from judgeaudit.data import load_examples
from judgeaudit.judge import grade_one, JUDGE_MODELS

OUT = Path("results/grades_track_a.jsonl")
OUT.parent.mkdir(exist_ok=True)

def conv_text(messages: list[dict]) -> str:
    return "\n\n".join(f"{m['role']}: {m['content']}" for m in messages)

def main():
    items = load_examples("meta_eval")
    random.Random(0).shuffle(items)
    items = items[:2000]
    
    # resumability: skip items already graded
    done = set()
    if OUT.exists():
        for line in open(OUT):
            r = json.loads(line)
            done.add((r["item_id"], r["judge_model"]))
    
    with open(OUT, "a") as f:
        for i, it in enumerate(items):
            criterion = it["rubric"]
            item_id = f'{it["completion_id"]}|{hashlib.sha1(str(criterion).encode()).hexdigest()[:8]}'
            convo = conv_text(it["prompt"])
            response = it["completion"]
            labels = it["binary_labels"]

            # skip ties: evenly split physician panel isn't ground truth
            if sum(labels) * 2 == len(labels):
                continue 

            label = sum(labels) > len(labels)/2 #majority vote
            theme = it.get("category", "unknown")

            for judge in JUDGE_MODELS:
                if (item_id, judge) in done:
                    continue
                grade = grade_one(judge, "v1_official", convo, response, criterion)
                f.write(json.dumps({"item_id": item_id,
                                    "prompt_id": it["prompt_id"],
                                    "judge_model": judge,
                                    "variant": "v1_official",
                                    "run_tag": "",
                                    "grade": grade,
                                    "physician_label": label, 
                                    "physician_agreement": sum(labels) / len(labels),
                                    "n_physicians": len(labels),
                                    "theme": theme,
                                    "response_len": len(response),
                }) + "\n")
            if (i + 1) % 50 == 0:
                print(f"{i+1}/{len(items)}")

if __name__ == "__main__":
    main()