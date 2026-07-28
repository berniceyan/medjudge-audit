import numpy as np
import pandas as pd

def cluster_bootstrap(df: pd.DataFrame, stat_fn, cluster_col: str = "prompt_id",
                      n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """(point, ci_low, ci_high) for stat_fn(df), resampling whole clusters with replacement. 
    Clusters = conversations: Conversations are the true independent units.
    All evaluation rows belonging to the same conversation share difficulty and 
    should be kept together during statistical resampling."""
    rng = np.random.default_rng(seed)
    df = df.reset_index(drop=True)
    idx = {c: g.to_numpy() for c, g in df.groupby(cluster_col).groups.items()}
    clusters = np.array(list(idx.keys()), dtype=object)
    stats = np.empty(n_boot)
    for b in range(n_boot):
        chosen = rng.choice(clusters, size=len(clusters), replace=True)
        rows = np.concatenate([idx[c] for c in chosen])
        stats[b] = stat_fn(df.iloc[rows])
    lo, hi = np.nanpercentile(stats, [2.5, 97.5])
    return stat_fn(df), lo, hi

def naive_bootstrap(df: pd.DataFrame, stat_fn, n_boot: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """Row-level resampling — WRONG for clustered data. Exists as comparison."""
    rng = np.random.default_rng(seed)
    df = df.reset_index(drop=True)
    stats = np.empty(n_boot)
    for b in range(n_boot):
        rows = rng.integers(0, len(df), len(df))
        stats[b] = stat_fn(df.iloc[rows])
    lo, hi = np.nanpercentile(stats, [2.5, 97.5])
    return stat_fn(df), lo, hi