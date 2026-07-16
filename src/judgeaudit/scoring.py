import numpy as np
import pandas as pd

def example_score(g: pd.DataFrame) -> float:
    """g: the grade rows for ONE (prompt_id, response_model, judge, variant, run_tag). Needs columns: grade (bool), points (int)."""
    g = g[g.grade.notna()]
    earned = g.loc[g.grade.astype(bool), "points"].sum()
    possible = g.loc[g.points > 0, "points"].sum()
    return max(0.0, earned / possible) if possible > 0 else np.nan

def per_example_scores(b: pd.DataFrame) -> pd.DataFrame:
    """One row per (config, example): the unit of analysis for everything below.""" 
    keys = ["response_model", "judge_model", "variant", "run_tag", "prompt_id"] 
    return (b.groupby(keys).apply(example_score)
            .rename("score").reset_index())