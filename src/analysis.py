"""Statistical analysis tools for Monte Carlo results.

This module provides functions for computing confidence intervals,
overbudget probabilities, and summary statistics from an array of
simulated cost samples.
"""

import numpy as np
from scipy import stats


def compute_ci(
    samples: np.ndarray, alpha: float = 0.05
) -> tuple[float, float]:
    """Compute a confidence interval for the population mean using the CLT.

    Parameters
    ----------
    samples : np.ndarray
        Array of simulated cost values.
    alpha : float
        Significance level. Default 0.05 gives a 95% CI.

    Returns
    -------
    tuple[float, float]
        (lower_bound, upper_bound) of the confidence interval.

    Notes
    -----
    Uses the CLT approximation:

    .. math::
        \\bar{X} \\pm z_{\\alpha/2} \\cdot \\frac{s}{\\sqrt{N}}

    Examples
    --------
    >>> rng = np.random.default_rng(42)
    >>> samples = rng.normal(100, 10, size=1000)
    >>> lo, hi = compute_ci(samples, alpha=0.05)
    >>> lo < 100 < hi
    True
    """
    n = len(samples)
    x_bar = float(np.mean(samples))
    s = float(np.std(samples, ddof=1))
    z = stats.norm.ppf(1 - alpha / 2)
    margin = z * s / np.sqrt(n)
    return (x_bar - margin, x_bar + margin)


def prob_over_budget(samples: np.ndarray, budget: float) -> float:
    """Estimate the probability that the cost exceeds a budget ceiling.

    Parameters
    ----------
    samples : np.ndarray
        Array of simulated cost values.
    budget : float
        Budget ceiling in the same units as samples.

    Returns
    -------
    float
        Estimated P(X > budget) as a fraction in [0, 1].

    Examples
    --------
    >>> samples = np.array([100, 200, 300, 400, 500])
    >>> prob_over_budget(samples, 250)
    0.6
    """
    return float(np.mean(samples > budget))


def summary_stats(samples: np.ndarray) -> dict[str, float]:
    """Compute summary statistics for simulated costs.

    Parameters
    ----------
    samples : np.ndarray
        Array of simulated cost values.

    Returns
    -------
    dict[str, float]
        Dictionary with keys: mean, std, se, median, p5, p25, p75, p95,
        min, max, skewness, kurtosis.
    """
    n = len(samples)
    return {
        "mean": float(np.mean(samples)),
        "std": float(np.std(samples, ddof=1)),
        "se": float(np.std(samples, ddof=1) / np.sqrt(n)),
        "median": float(np.median(samples)),
        "p5": float(np.percentile(samples, 5)),
        "p25": float(np.percentile(samples, 25)),
        "p75": float(np.percentile(samples, 75)),
        "p95": float(np.percentile(samples, 95)),
        "min": float(np.min(samples)),
        "max": float(np.max(samples)),
        "skewness": float(stats.skew(samples)),
        "kurtosis": float(stats.kurtosis(samples)),
    }
