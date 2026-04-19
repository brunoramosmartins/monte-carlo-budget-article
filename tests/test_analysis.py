"""Tests for statistical analysis tools (src/analysis.py)."""

import numpy as np
import pytest

from src.analysis import compute_ci, prob_over_budget, summary_stats


class TestComputeCI:
    """Test confidence interval computation."""

    def test_ci_contains_known_mean(self) -> None:
        """95% CI from N(100, 10²) should contain 100."""
        rng = np.random.default_rng(42)
        samples = rng.normal(100, 10, size=5000)
        lo, hi = compute_ci(samples, alpha=0.05)
        assert lo < 100 < hi

    def test_ci_width_decreases_with_n(self) -> None:
        rng = np.random.default_rng(42)
        small = rng.normal(100, 10, size=100)
        large = rng.normal(100, 10, size=10_000)
        width_small = compute_ci(small)[1] - compute_ci(small)[0]
        width_large = compute_ci(large)[1] - compute_ci(large)[0]
        assert width_large < width_small

    def test_wider_ci_at_higher_confidence(self) -> None:
        rng = np.random.default_rng(42)
        samples = rng.normal(100, 10, size=1000)
        w_90 = compute_ci(samples, alpha=0.10)
        w_99 = compute_ci(samples, alpha=0.01)
        width_90 = w_90[1] - w_90[0]
        width_99 = w_99[1] - w_99[0]
        assert width_99 > width_90

    def test_ci_coverage_over_many_trials(self) -> None:
        """Empirical coverage should be near 95% over 500 trials."""
        true_mean = 100.0
        n_trials = 500
        n_samples = 200
        hits = 0
        for seed in range(n_trials):
            rng = np.random.default_rng(seed)
            samples = rng.normal(true_mean, 10, size=n_samples)
            lo, hi = compute_ci(samples, alpha=0.05)
            if lo <= true_mean <= hi:
                hits += 1
        coverage = hits / n_trials
        assert 0.90 < coverage < 0.99, f"Coverage {coverage:.3f} out of range"

    def test_ci_returns_tuple_of_floats(self) -> None:
        samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        lo, hi = compute_ci(samples)
        assert isinstance(lo, float)
        assert isinstance(hi, float)
        assert lo < hi


class TestProbOverBudget:
    """Test overbudget probability estimation."""

    def test_all_below(self) -> None:
        samples = np.array([100, 200, 300])
        assert prob_over_budget(samples, 500) == 0.0

    def test_all_above(self) -> None:
        samples = np.array([100, 200, 300])
        assert prob_over_budget(samples, 50) == 1.0

    def test_partial(self) -> None:
        samples = np.array([100, 200, 300, 400, 500])
        assert prob_over_budget(samples, 250) == pytest.approx(0.6)

    def test_returns_float(self) -> None:
        samples = np.array([1.0, 2.0, 3.0])
        result = prob_over_budget(samples, 2.5)
        assert isinstance(result, float)


class TestSummaryStats:
    """Test summary statistics computation."""

    def test_keys_present(self) -> None:
        samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        s = summary_stats(samples)
        expected_keys = {
            "mean", "std", "se", "median",
            "p5", "p25", "p75", "p95",
            "min", "max", "skewness", "kurtosis",
        }
        assert set(s.keys()) == expected_keys

    def test_mean_value(self) -> None:
        samples = np.array([10.0, 20.0, 30.0])
        s = summary_stats(samples)
        assert s["mean"] == pytest.approx(20.0)

    def test_median_value(self) -> None:
        samples = np.array([10.0, 20.0, 30.0])
        s = summary_stats(samples)
        assert s["median"] == pytest.approx(20.0)

    def test_min_max(self) -> None:
        samples = np.array([5.0, 10.0, 15.0, 20.0])
        s = summary_stats(samples)
        assert s["min"] == 5.0
        assert s["max"] == 20.0

    def test_all_values_are_floats(self) -> None:
        rng = np.random.default_rng(42)
        samples = rng.normal(0, 1, size=100)
        s = summary_stats(samples)
        for key, val in s.items():
            assert isinstance(val, float), f"{key} is {type(val)}"
