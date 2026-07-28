import numpy as np
from sklearn.metrics import cohen_kappa_score
from judgeaudit.agreement import cohens_kappa

def test_kappa_matches_sklearn():
    rng = np.random.default_rng(0)
    y1 = rng.integers(0, 2, 200).astype(bool)
    y2 = rng.integers(0, 2, 200).astype(bool)
    assert abs(cohens_kappa(y1, y2) - cohen_kappa_score(y1, y2)) < 1e-9