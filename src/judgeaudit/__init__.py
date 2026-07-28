"""judgeaudit — a reliability audit toolkit for LLM-as-judge rubric evals.

Public API:
    report_card(track_a, track_b=None) -> markdown reliability report
    cluster_bootstrap(df, stat_fn, ...) -> (point, ci_low, ci_high)
    power_curve(paired_diffs, ...)      -> {(delta, n): power}
"""
from judgeaudit.report import report_card
from judgeaudit.uncertainty import cluster_bootstrap
from judgeaudit.power import power_curve

__all__ = ["report_card", "cluster_bootstrap", "power_curve"]
