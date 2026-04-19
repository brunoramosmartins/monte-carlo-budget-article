"""Tests for variance reduction techniques (src/variance_reduction.py)."""

import numpy as np
import pytest

from src.model import BudgetModel
from src.monte_carlo import MonteCarloResult, MonteCarloSimulator
from src.variance_reduction import (
    antithetic_mc,
    control_variate_mc,
    stratified_mc,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def model() -> BudgetModel:
    return BudgetModel()


def _budget_cost_fn(model: BudgetModel):
    """Return a cost function closure for the budget model."""
    return lambda rng: model.simulate_one_year(rng).total_cost


def _salary_control_fn(model: BudgetModel):
    """Return a control function that extracts total raw salaries."""
    def fn(rng: np.random.Generator) -> float:
        result = model.simulate_one_year(rng)
        # Reverse-engineer raw salary sum from salary_cost
        return result.salary_cost / (model.params.benefits_multiplier * 12)
    return fn


# ---------------------------------------------------------------------------
# Antithetic variates
# ---------------------------------------------------------------------------


class TestAntitheticMC:
    def test_returns_monte_carlo_result(self, model: BudgetModel) -> None:
        result = antithetic_mc(_budget_cost_fn(model), n_pairs=50, seed=42)
        assert isinstance(result, MonteCarloResult)

    def test_correct_sample_count(self, model: BudgetModel) -> None:
        result = antithetic_mc(_budget_cost_fn(model), n_pairs=100, seed=42)
        assert len(result.samples) == 200
        assert result.n_iterations == 200

    def test_reproducibility(self, model: BudgetModel) -> None:
        r1 = antithetic_mc(_budget_cost_fn(model), n_pairs=50, seed=42)
        r2 = antithetic_mc(_budget_cost_fn(model), n_pairs=50, seed=42)
        np.testing.assert_array_equal(r1.samples, r2.samples)

    def test_all_samples_positive(self, model: BudgetModel) -> None:
        result = antithetic_mc(_budget_cost_fn(model), n_pairs=100, seed=42)
        assert np.all(result.samples > 0)

    def test_mean_reasonable(self, model: BudgetModel) -> None:
        """Mean should be within 5% of analytical."""
        result = antithetic_mc(_budget_cost_fn(model), n_pairs=2500, seed=42)
        analytical = model.analytical_expected_total()
        rel_error = abs(result.mean - analytical) / analytical
        assert rel_error < 0.05


# ---------------------------------------------------------------------------
# Control variates
# ---------------------------------------------------------------------------


class TestControlVariateMC:
    def test_returns_monte_carlo_result(self, model: BudgetModel) -> None:
        e_salary_sum = model.params.n_employees * np.exp(
            model.params.mu_salary + model.params.sigma_salary**2 / 2
        )
        result = control_variate_mc(
            cost_fn=_budget_cost_fn(model),
            control_fn=_salary_control_fn(model),
            control_mean=e_salary_sum,
            n_iterations=100,
            seed=42,
        )
        assert isinstance(result, MonteCarloResult)

    def test_correct_sample_count(self, model: BudgetModel) -> None:
        e_salary_sum = model.params.n_employees * np.exp(
            model.params.mu_salary + model.params.sigma_salary**2 / 2
        )
        result = control_variate_mc(
            cost_fn=_budget_cost_fn(model),
            control_fn=_salary_control_fn(model),
            control_mean=e_salary_sum,
            n_iterations=500,
            seed=42,
        )
        assert len(result.samples) == 500

    def test_reproducibility(self, model: BudgetModel) -> None:
        e_salary_sum = model.params.n_employees * np.exp(
            model.params.mu_salary + model.params.sigma_salary**2 / 2
        )
        kwargs = dict(
            cost_fn=_budget_cost_fn(model),
            control_fn=_salary_control_fn(model),
            control_mean=e_salary_sum,
            n_iterations=200,
            seed=42,
        )
        r1 = control_variate_mc(**kwargs)
        r2 = control_variate_mc(**kwargs)
        np.testing.assert_array_equal(r1.samples, r2.samples)

    def test_variance_reduction(self, model: BudgetModel) -> None:
        """Control variate std should be less than naive MC std."""
        n = 5_000
        e_salary_sum = model.params.n_employees * np.exp(
            model.params.mu_salary + model.params.sigma_salary**2 / 2
        )

        # Naive MC
        naive = MonteCarloSimulator(_budget_cost_fn(model)).run(n, seed=42)

        # Control variate MC
        cv = control_variate_mc(
            cost_fn=_budget_cost_fn(model),
            control_fn=_salary_control_fn(model),
            control_mean=e_salary_sum,
            n_iterations=n,
            seed=42,
        )

        assert cv.std < naive.std, (
            f"CV std ({cv.std:.0f}) should be < naive std ({naive.std:.0f})"
        )


# ---------------------------------------------------------------------------
# Stratified sampling
# ---------------------------------------------------------------------------


class TestStratifiedMC:
    def test_returns_monte_carlo_result(self) -> None:
        def simple_fn(rng: np.random.Generator, stratum: int) -> float:
            shift = stratum * 10.0
            return float(rng.normal(100 + shift, 5))

        result = stratified_mc(simple_fn, n_strata=3, n_per_stratum=50, seed=42)
        assert isinstance(result, MonteCarloResult)

    def test_correct_sample_count(self) -> None:
        def simple_fn(rng: np.random.Generator, stratum: int) -> float:
            return float(rng.normal(100, 10))

        result = stratified_mc(simple_fn, n_strata=3, n_per_stratum=100, seed=42)
        assert len(result.samples) == 300
        assert result.n_iterations == 300

    def test_reproducibility(self) -> None:
        def simple_fn(rng: np.random.Generator, stratum: int) -> float:
            return float(rng.normal(100, 10))

        r1 = stratified_mc(simple_fn, n_strata=3, n_per_stratum=100, seed=42)
        r2 = stratified_mc(simple_fn, n_strata=3, n_per_stratum=100, seed=42)
        np.testing.assert_array_equal(r1.samples, r2.samples)

    def test_mean_close_to_known(self) -> None:
        """With known stratum means, overall mean should be close."""
        def fn(rng: np.random.Generator, stratum: int) -> float:
            means = [90.0, 100.0, 110.0]
            return float(rng.normal(means[stratum], 5))

        result = stratified_mc(fn, n_strata=3, n_per_stratum=1000, seed=42)
        assert result.mean == pytest.approx(100.0, abs=2.0)


# ---------------------------------------------------------------------------
# Known-distribution tests (simpler, verifiable)
# ---------------------------------------------------------------------------


class TestVarianceReductionOnKnownDistribution:
    """Test on Normal(100, 10²) where we can verify analytically."""

    def test_control_variate_with_perfect_control(self) -> None:
        """If h = g (perfect correlation), variance should be near zero."""
        fn = lambda rng: float(rng.normal(100, 10))
        result = control_variate_mc(
            cost_fn=fn,
            control_fn=fn,  # h = g, perfect correlation
            control_mean=100.0,
            n_iterations=1000,
            seed=42,
        )
        # With perfect control, adjusted samples should cluster near the mean
        assert result.std < 1.0, f"Std should be near 0, got {result.std:.4f}"
