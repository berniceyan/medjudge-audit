import numpy as np

def power_curve(paired_diffs: np.ndarray, deltas=(0.01, 0.02, 0.05), 
                ns=(100, 200, 400, 800), n_sim=1000, seed=0) -> dict:
    """paired_diffs: real per-example score differences between 
    two models (same examples, same judge). Returns {(delta, n): power}.
    Note: one difference per example = clustering handled by construction.""" 
    rng = np.random.default_rng(seed)
    noise = paired_diffs - paired_diffs.mean()
    results = {}
    for delta in deltas:
        for n in ns: 
            detected = 0
            for _ in range(n_sim):
                d = rng.choice(noise, size=n, replace=True) + delta
                se = d.std(ddof=1) / np.sqrt(n) # paired t-test on the mean diff 
                if abs(d.mean()) > 1.96 * se:
                    detected += 1
            results[(delta, n)] = detected / n_sim
    return results

def min_detectable_effect(paired_diffs: np.ndarray, n: int, power: float = 0.8) -> float:
    """Standard MDE formula: the smallest true gap detectable with given power. 2.80 = z_{0.975} + z_{0.80}."""
    return 2.80 * paired_diffs.std(ddof=1) / np.sqrt(n)