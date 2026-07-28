import pandas as pd
from judgeaudit.scoring import per_example_scores


def _avg_spread(ex: pd.DataFrame, factor: str) -> float:
    """Average (over response models) of the max-min spread of per-example score
    means across `factor`. Complete-case: for each model, only examples graded at
    EVERY level of `factor` are used, so the levels are compared on the same
    examples. Returns NaN if `factor` has <2 levels present."""
    spreads = []
    for _, g in ex.groupby("response_model"):
        wide = g.pivot_table(index="prompt_id", columns=factor, values="score").dropna()
        if wide.shape[1] > 1 and len(wide) > 0:
            means = wide.mean()  # column means over the common examples
            spreads.append(float(means.max() - means.min()))
    return sum(spreads) / len(spreads) if spreads else float("nan")


def variance_panel(track_b: pd.DataFrame, ref_judge: str, ref_variant: str,
                   baseline_tag: str = "") -> dict:
    """Four headline numbers from a grid of grades (B1+B2+B3 concatenated).

    ref_judge / ref_variant define the canonical config that the nuisance factors
    are varied around; baseline_tag is the run_tag of the non-repeated baseline
    (repeats are any other run_tag, e.g. 'rep0'..'rep4').

    Returns dict with: model_gap, and spreads for 'sampling reps',
    'judge choice', 'prompt wording'.
    """
    ex = per_example_scores(track_b)

    # Model gap: difference between response-model mean scores at the reference cell.
    ref = ex[(ex.judge_model == ref_judge) & (ex.variant == ref_variant)
             & (ex.run_tag == baseline_tag)]
    gm = ref.groupby("response_model").score.mean()
    model_gap = float(gm.max() - gm.min())

    # Each spread holds the other two factors at the reference and varies one:
    rep = _avg_spread(
        ex[(ex.judge_model == ref_judge) & (ex.variant == ref_variant)
           & (ex.run_tag != baseline_tag)], "run_tag")       # temp-1 repeats only
    judge = _avg_spread(
        ex[(ex.variant == ref_variant) & (ex.run_tag == baseline_tag)], "judge_model")
    variant = _avg_spread(
        ex[(ex.judge_model == ref_judge) & (ex.run_tag == baseline_tag)], "variant")

    return {"model_gap": model_gap, "sampling reps": rep,
            "judge choice": judge, "prompt wording": variant}
