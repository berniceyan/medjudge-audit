import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

def cohens_kappa(y1: np.ndarray, y2: np.ndarray) -> float:
    po = (y1 == y2).mean()  # observed agreement
    p1, p2 = y1.mean(), y2.mean() # P(True) for each rater
    pe = p1 * p2 + (1 - p1) * (1 - p2)  # expected agreement; chance both True + both False
    return (po - pe) / (1 - pe)

# to prevent kappa denominator from approaching 0 if a stratum's labels are nearly all one class (chance agreement would approach 1)
def safe_kappa(y1, y2):
    po = (y1 == y2).mean()
    p1, p2 = y1.mean(), y2.mean()
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    return np.nan if pe >= 0.999 else (po - pe) / (1 - pe)


def agreement_panel(track_a: pd.DataFrame, variant: str = "v1_official") -> pd.DataFrame:
    """5a table: one row per judge with raw agreement, Cohen's kappa, and macro-F1
    against the physician labels. Uses only the given (official) prompt variant and
    drops unparseable grades. Needs columns: judge_model, variant, grade,
    physician_label."""
    v = track_a[(track_a.variant == variant) & track_a.grade.notna()]
    rows = []
    for judge, g in v.groupby("judge_model"):
        y_md = g.physician_label.to_numpy()
        y_j = g.grade.astype(bool).to_numpy()
        rows.append({
            "judge": judge,
            "pct_agree": (y_md == y_j).mean(),
            "kappa": cohens_kappa(y_md, y_j),
            "macro_f1": f1_score(y_md, y_j, average="macro"),
        })
    return pd.DataFrame(rows).sort_values("kappa", ascending=False)