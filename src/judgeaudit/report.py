import pandas as pd
from judgeaudit.agreement import agreement_panel
from judgeaudit.uncertainty import cluster_bootstrap
from judgeaudit.scoring import per_example_scores
from judgeaudit.variance import variance_panel
from judgeaudit.power import min_detectable_effect


def _df_to_md(df: pd.DataFrame) -> str:
    """Render a DataFrame as a markdown table (no tabulate dep).
    Floats are shown to 3 decimals."""
    def fmt(x):
        return f"{x:.3f}" if isinstance(x, float) else str(x)
    header = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    rows = ["| " + " | ".join(fmt(x) for x in r) + " |"
            for r in df.itertuples(index=False)]
    return "\n".join([header, sep, *rows])


def report_card(track_a: pd.DataFrame, track_b: pd.DataFrame | None = None, *,
                ref_judge: str = "openai/gpt-4.1",
                ref_variant: str = "v1_official") -> str:
    """Judge-reliability report card.

    track_a: judge-vs-physician grades (needs judge_model, variant, grade,
             physician_label, prompt_id). Drives sections 1-2.
    track_b: model-comparison grid of grades (B1+B2+B3 concatenated; needs
             response_model, judge_model, variant, run_tag, criterion_idx,
             points, grade, prompt_id). Drives sections 3-4.
    ref_judge / ref_variant: the canonical config sections 2-4 are anchored on.
    """
    md = ["# Judge Reliability Report Card"]

    # 1. Agreement with human labels ------------------------------------------
    md.append("## 1. Agreement with human labels")
    md.append(_df_to_md(agreement_panel(track_a, variant=ref_variant)))

    # 2. Uncertainty (clustered 95% CIs) --------------------------------------
    md.append("## 2. Uncertainty (clustered 95% CIs)")
    a_ref = track_a[track_a.variant == ref_variant]
    for judge, g in a_ref.groupby("judge_model"):
        pt, lo, hi = cluster_bootstrap(
            g, lambda d: (d.grade == d.physician_label).mean(),
            cluster_col="prompt_id")  # criteria in one conversation are correlated
        md.append(f"- {judge}: agreement {pt:.3f} [{lo:.3f}, {hi:.3f}]")

    if track_b is not None:
        v = variance_panel(track_b, ref_judge=ref_judge, ref_variant=ref_variant)
        gap = v["model_gap"]

        # 3. Sensitivity -------------------------------------------------------
        md.append("## 3. Sensitivity (movement in score from config choices)")
        table = ["| source | spread | vs model gap |", "|---|---|---|"]
        for k in ("sampling reps", "judge choice", "prompt wording"):
            table.append(f"| {k} | {v[k]:.3f} | {v[k] / gap:.0%} |")
        table.append(f"| **MODEL GAP** | **{gap:.3f}** | — |")
        md.append("\n".join(table))  # one block so the table renders

        # 4. Power -------------------------------------------------------------
        md.append("## 4. Power")
        ex = per_example_scores(track_b)
        ref = ex[(ex.judge_model == ref_judge) & (ex.variant == ref_variant)
                 & (ex.run_tag == "")]
        wide = ref.pivot_table(index="prompt_id", columns="response_model",
                               values="score")
        diffs = (wide.iloc[:, 0] - wide.iloc[:, 1]).dropna().to_numpy()
        n = len(diffs)
        mde = min_detectable_effect(diffs, n)
        verdict = "detectable" if gap > mde else "NOT detectable"
        md.append(f"- n={n}: minimum detectable gap ~{mde:.3f} at 80% power. "
                  f"Observed model gap {gap:.3f} is **{verdict}** at this n.")

    return "\n\n".join(md)
