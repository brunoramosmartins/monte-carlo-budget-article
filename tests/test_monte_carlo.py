"""Tests for the Monte Carlo simulation engine (src/monte_carlo.py)."""

import numpy as np
import pytest

from src.model import BudgetModel
from src.monte_carlo import MonteCarloResult, MonteCarloSimulator


@pytest.fixture
def budget_simulator() -> MonteCarloSimulator:
    """Create a MonteCarloSimulator with the default budget model."""
    model = BudgetModel()
    return MonteCarloSimulator(
        cost_fn=lambda rng: model.simulate_one_year(rng).total_cost
    )


class TestMonteCarloSimulator:
    """Test the Monte Carlo engine."""

    def test_run_returns_result(self, budget_simulator: MonteCarloSimulator) -> None:
        result = budget_simulator.run(n_iterations=100, seed=42)
        assert isinstance(result, MonteCarloResult)

    def test_correct_number_of_samples(
        self, budget_simulator: MonteCarloSimulator
    ) -> None:
        result = budget_simulator.run(n_iterations=500, seed=42)
        assert len(result.samples) == 500
        assert result.n_iterations == 500

    def test_seed_stored(self, budget_simulator: MonteCarloSimulator) -> None:
        result = budget_simulator.run(n_iterations=100, seed=99)
        assert result.seed == 99

    def test_reproducibility(self, budget_simulator: MonteCarloSimulator) -> None:
        r1 = budget_simulator.run(n_iterations=200, seed=42)
        r2 = budget_simulator.run(n_iterations=200, seed=42)
        np.testing.assert_array_equal(r1.samples, r2.samples)

    def test_different_seeds_differ(
        self, budget_simulator: MonteCarloSimulator
    ) -> None:
        r1 = budget_simulator.run(n_iterations=200, seed=1)
        r2 = budget_simulator.run(n_iterations=200, seed=2)
        assert not np.array_equal(r1.samples, r2.samples)

    def test_all_samples_positive(
        self, budget_simulator: MonteCarloSimulator
    ) -> None:
        result = budget_simulator.run(n_iterations=500, seed=42)
        assert np.all(result.samples > 0)


class TestMonteCarloResult:
    """Test MonteCarloResult computed properties."""

    def test_mean_property(self, budget_simulator: MonteCarloSimulator) -> None:
        result = budget_simulator.run(n_iterations=1000, seed=42)
        expected_mean = float(np.mean(result.samples))
        assert result.mean == pytest.approx(expected_mean, rel=1e-10)

    def test_std_property(self, budget_simulator: MonteCarloSimulator) -> None:
        result = budget_simulator.run(n_iterations=1000, seed=42)
        expected_std = float(np.std(result.samples, ddof=1))
        assert result.std == pytest.approx(expected_std, rel=1e-10)

    def test_standard_error_property(
        self, budget_simulator: MonteCarloSimulator
    ) -> None:
        result = budget_simulator.run(n_iterations=1000, seed=42)
        expected_se = result.std / np.sqrt(1000)
        assert result.standard_error == pytest.approx(expected_se, rel=1e-10)

    def test_standard_error_decreases_with_n(
        self, budget_simulator: MonteCarloSimulator
    ) -> None:
        r_small = budget_simulator.run(n_iterations=100, seed=42)
        r_large = budget_simulator.run(n_iterations=5000, seed=42)
        assert r_large.standard_error < r_small.standard_error


class TestMonteCarloWithSimpleFunction:
    """Test the engine with a known analytical answer."""

    def test_known_mean(self) -> None:
        """Normal(100, 10²) should have MC mean near 100."""
        sim = MonteCarloSimulator(
            cost_fn=lambda rng: float(rng.normal(100, 10))
        )
        result = sim.run(n_iterations=50_000, seed=42)
        assert result.mean == pytest.approx(100, abs=1.0)

    def test_known_std(self) -> None:
        """Normal(100, 10²) should have MC std near 10."""
        sim = MonteCarloSimulator(
            cost_fn=lambda rng: float(rng.normal(100, 10))
        )
        result = sim.run(n_iterations=50_000, seed=42)
        assert result.std == pytest.approx(10, abs=0.5)
