import numpy as np 

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