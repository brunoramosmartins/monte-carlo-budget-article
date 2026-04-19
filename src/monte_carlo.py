"""Monte Carlo simulation engine.

This module provides a generic Monte Carlo simulator that runs a cost model
function repeatedly and stores the results for analysis.

The engine is model-agnostic: it takes any callable that accepts an
``np.random.Generator`` and returns a float.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np


@dataclass
class MonteCarloResult:
    """Container for Monte Carlo simulation results.

    Attributes
    ----------
    samples : np.ndarray
        Array of simulated cost values, shape ``(n_iterations,)``.
    n_iterations : int
        Number of iterations run.
    seed : int
        Seed used for reproducibility.
    """

    samples: np.ndarray
    n_iterations: int
    seed: int

    @property
    def mean(self) -> float:
        """Sample mean of simulated costs."""
        return float(np.mean(self.samples))

    @property
    def std(self) -> float:
        """Sample standard deviation (ddof=1) of simulated costs."""
        return float(np.std(self.samples, ddof=1))

    @property
    def standard_error(self) -> float:
        """Monte Carlo standard error: s / sqrt(N)."""
        return self.std / np.sqrt(self.n_iterations)


class MonteCarloSimulator:
    """Generic Monte Carlo simulator.

    Runs a cost function ``n_iterations`` times with independent random
    draws and stores the raw results.

    Parameters
    ----------
    cost_fn : Callable[[np.random.Generator], float]
        A function that takes an RNG and returns a single simulated cost.
        For the budget model, this is typically
        ``lambda rng: model.simulate_one_year(rng).total_cost``.

    Examples
    --------
    >>> from src.model import BudgetModel
    >>> model = BudgetModel()
    >>> sim = MonteCarloSimulator(
    ...     cost_fn=lambda rng: model.simulate_one_year(rng).total_cost
    ... )
    >>> result = sim.run(n_iterations=1000, seed=42)
    >>> result.n_iterations
    1000
    """

    def __init__(
        self, cost_fn: Callable[[np.random.Generator], float]
    ) -> None:
        self.cost_fn = cost_fn

    def run(self, n_iterations: int, seed: int = 42) -> MonteCarloResult:
        """Run the Monte Carlo simulation.

        Parameters
        ----------
        n_iterations : int
            Number of independent simulation runs.
        seed : int
            Random seed for reproducibility.

        Returns
        -------
        MonteCarloResult
            Container with raw samples and metadata.
        """
        rng = np.random.default_rng(seed)
        samples = np.array(
            [self.cost_fn(rng) for _ in range(n_iterations)]
        )
        return MonteCarloResult(
            samples=samples,
            n_iterations=n_iterations,
            seed=seed,
        )
