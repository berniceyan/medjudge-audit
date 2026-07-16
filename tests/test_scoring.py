import pandas as pd
from judgeaudit.scoring import example_score

def _df(rows):
    return pd.DataFrame(rows, columns=["grade", "points"])

def test_basic_scoring():
    g = _df([(True, 5), (False, 3), (True, -2)]) 
    assert abs(example_score(g) - 3/8) < 1e-9

def test_clip_at_zero():
    g = _df([(False, 5), (True, -4)]) 
    assert example_score(g) == 0.0

def test_unparseable_rows_excluded(): 
    g = _df([(True, 5), (None, 5)])
    assert example_score(g) == 1.0
    