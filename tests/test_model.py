"""Tests for the budget cost model (src/model.py)."""

import numpy as np
import pytest

from src.model import BudgetModel, BudgetModelParams, YearResult


class TestBudgetModelParams:
    """Test default parameter values."""

    def test_defaults_match_spec(self) -> None:
        p = BudgetModelParams()
        assert p.n_employees == 50
        assert p.mu_salary == 9.2
        assert p.sigma_salary == 0.3
        assert p.benefits_multiplier == 1.80
        assert p.lambda_overtime == 5.0
        assert p.overtime_hourly_rate == 80.0
        assert p.lambda_incidents == 3.0
        assert p.mu_incident_cost == 10.5
        assert p.sigma_incident_cost == 0.5


class TestBudgetModel:
    """Test the BudgetModel simulation."""

    def test_simulate_returns_year_result(self) -> None:
        model = BudgetModel()
        rng = np.random.default_rng(42)
        result = model.simulate_one_year(rng)
        assert isinstance(result, YearResult)

    def test_all_costs_positive(self) -> None:
        model = BudgetModel()
        rng = np.random.default_rng(42)
        result = model.simulate_one_year(rng)
        assert result.salary_cost > 0
        assert result.overtime_cost > 0
        assert result.total_cost > 0
        # incident_cost can be 0 if no incidents occur

    def test_total_equals_sum_of_components(self) -> None:
        model = BudgetModel()
        rng = np.random.default_rng(42)
        result = model.simulate_one_year(rng)
        expected = result.salary_cost + result.overtime_cost + result.incident_cost
        assert result.total_cost == pytest.approx(expected, rel=1e-10)

    def test_reproducibility_with_same_seed(self) -> None:
        model = BudgetModel()
        r1 = model.simulate_one_year(np.random.default_rng(123))
        r2 = model.simulate_one_year(np.random.default_rng(123))
        assert r1.total_cost == r2.total_cost

    def test_different_seeds_give_different_results(self) -> None:
        model = BudgetModel()
        r1 = model.simulate_one_year(np.random.default_rng(1))
        r2 = model.simulate_one_year(np.random.default_rng(2))
        assert r1.total_cost != r2.total_cost

    def test_sample_mean_near_analytical(self) -> None:
        """Monte Carlo mean should be within 2% of analytical E[X]."""
        model = BudgetModel()
        rng = np.random.default_rng(42)
        n = 10_000
        costs = [model.simulate_one_year(rng).total_cost for _ in range(n)]
        sample_mean = np.mean(costs)
        analytical = model.analytical_expected_total()
        relative_error = abs(sample_mean - analytical) / analytical
        assert relative_error < 0.02, (
            f"Sample mean {sample_mean:.0f} too far from "
            f"analytical {analytical:.0f} (error {relative_error:.4%})"
        )

    def test_zero_incidents_possible(self) -> None:
        """With lambda_incidents=0, incident cost should always be 0."""
        params = BudgetModelParams(lambda_incidents=0.0)
        model = BudgetModel(params)
        rng = np.random.default_rng(42)
        result = model.simulate_one_year(rng)
        assert result.incident_cost == 0.0
        assert result.n_incidents == 0

    def test_custom_params(self) -> None:
        params = BudgetModelParams(n_employees=10, benefits_multiplier=1.50)
        model = BudgetModel(params)
        assert model.params.n_employees == 10
        assert model.params.benefits_multiplier == 1.50


class TestAnalyticalMoments:
    """Test analytical moment computations."""

    def test_analytical_expected_total_positive(self) -> None:
        model = BudgetModel()
        assert model.analytical_expected_total() > 0

    def test_analytical_variance_total_positive(self) -> None:
        model = BudgetModel()
        assert model.analytical_variance_total() > 0

    def test_analytical_expected_matches_model_design(self) -> None:
        """E[X_total] should be approximately R$ 11.55M per docs/model-design.md."""
        model = BudgetModel()
        e_total = model.analytical_expected_total()
        assert 11_000_000 < e_total < 12_000_000, (
            f"E[X_total] = {e_total:.0f} outside expected range"
        )
