# scripts/make_report.py — assemble the report card from all tracks.
import pandas as pd
from pathlib import Path
from judgeaudit.report import report_card

track_a = pd.read_json("results/grades_track_a.jsonl", lines=True)

# track_b is the whole model-comparison grid: B1 (v1 baseline) + B2 (judge/prompt
# grid) + B3 (temp-1 repeats), stacked into one frame with the shared row schema.
track_b = pd.concat([
    pd.read_json("results/grades_track_b1.jsonl", lines=True),
    pd.read_json("results/grades_track_b2.jsonl", lines=True),
    pd.read_json("results/grades_track_b3.jsonl", lines=True),
], ignore_index=True)

md = report_card(track_a, track_b,
                 ref_judge="openai/gpt-4.1", ref_variant="v1_official")

out = Path("results/report_card.md")
out.write_text(md)
print(md)
print(f"\n[written to {out}]")
