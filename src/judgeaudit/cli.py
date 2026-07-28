import argparse
import pandas as pd
from judgeaudit.report import report_card


def main():
    p = argparse.ArgumentParser(
        prog="judgeaudit",
        description="Reliability report card for LLM judges on rubric evals")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("report", help="grades jsonl -> markdown report")
    r.add_argument("grades", help="Track A grades jsonl (agreement vs physicians)")
    r.add_argument("-b", "--track-b", default=None,
                   help="optional Track B grid jsonl; adds the sensitivity + power sections")
    r.add_argument("-o", "--out", default="report.md")
    r.add_argument("--ref-judge", default="openai/gpt-4.1",
                   help="canonical judge the sensitivity/power sections anchor on")
    r.add_argument("--ref-variant", default="v1_official",
                   help="canonical prompt variant")

    args = p.parse_args()
    if args.cmd == "report":
        track_a = pd.read_json(args.grades, lines=True)
        track_b = pd.read_json(args.track_b, lines=True) if args.track_b else None
        md = report_card(track_a, track_b,
                         ref_judge=args.ref_judge, ref_variant=args.ref_variant)
        with open(args.out, "w") as f:
            f.write(md)
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
