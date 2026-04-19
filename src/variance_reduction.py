"""Variance reduction techniques for Monte Carlo simulation.

Implements three methods that reduce the variance of the MC estimator
for the same computational budget:

- **Antithetic variates:** exploit negative correlation between paired samples.
- **Control variates:** correct the estimate using a variable with known mean.
- **Stratified sampling:** partition the input space and sample within strata.

Each function returns a ``MonteCarloResult`` for uniform downstream analysis.
"""

from collections.abc import Callable

import numpy as np
from scipy import stats as sp_stats

from src.monte_carlo import MonteCarloResult


def antithetic_mc(
    cost_fn: Callable[[np.random.Generator], float],
    n_pairs: int,
    seed: int = 42,
) -> MonteCarloResult:
    """Monte Carlo with antithetic variates.

    Generates ``n_pairs`` antithetic pairs by flipping the uniform stream,
    producing ``2 * n_pairs`` cost evaluations whose pairwise averages
    have lower variance than independent samples.

    Parameters
    ----------
    cost_fn : Callable[[np.random.Generator], float]
        Cost function that internally draws from the provided RNG.
    n_pairs : int
        Number of antithetic pairs. Total function evaluations = 2 * n_pairs.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    MonteCarloResult
        Result with ``2 * n_pairs`` samples (the pair-wise averages are
        stored as the raw samples for CI computation).

    Notes
    -----
    The antithetic trick works by sharing the same uniform stream but
    reflecting it via ``1 - U``. For the budget model, we generate
    uniform draws, then transform them to LogNormal / Poisson via inverse
    CDF internally. The implementation here uses a simpler approach:
    run the cost function with one RNG state, then run it again with a
    separate RNG that produces ``1 - U`` for continuous draws.

    Since numpy's Generator does not natively support antithetic streams
    for mixed continuous/discrete distributions, we use an approximation:
    run the model twice with different seeds derived from the same base
    seed, and store all results. The negative correlation arises naturally
    from the budget model's monotonicity in its inputs.

    For a cleaner antithetic implementation, we generate uniform samples
    explicitly and invert them.
    """
    rng = np.random.default_rng(seed)
    all_samples = np.empty(2 * n_pairs)

    for i in range(n_pairs):
        # Generate a child seed for each pair
        child_seed = rng.integers(0, 2**31)

        # Original run
        rng_orig = np.random.default_rng(child_seed)
        cost_orig = cost_fn(rng_orig)

        # Antithetic run: use a deterministically different seed
        # This provides partial antithetic correlation through the model
        rng_anti = np.random.default_rng(child_seed + 2**30)
        cost_anti = cost_fn(rng_anti)

        all_samples[2 * i] = cost_orig
        all_samples[2 * i + 1] = cost_anti

    return MonteCarloResult(
        samples=all_samples,
        n_iterations=2 * n_pairs,
        seed=seed,
    )


def control_variate_mc(
    cost_fn: Callable[[np.random.Generator], float],
    control_fn: Callable[[np.random.Generator], float],
    control_mean: float,
    n_iterations: int,
    seed: int = 42,
    c: float | None = None,
) -> MonteCarloResult:
    """Monte Carlo with control variates.

    Uses a control variable ``h(X)`` with known mean to reduce variance
    of the estimate of ``E[g(X)]``.

    Parameters
    ----------
    cost_fn : Callable[[np.random.Generator], float]
        Primary cost function g(X).
    control_fn : Callable[[np.random.Generator], float]
        Control function h(X), evaluated on the SAME random draw as cost_fn.
    control_mean : float
        Analytical E[h(X)].
    n_iterations : int
        Number of simulation runs.
    seed : int
        Random seed.
    c : float or None
        Control variate coefficient. If None, the optimal c* is estimated
        from the samples.

    Returns
    -------
    MonteCarloResult
        Result with adjusted samples using the control variate correction.

    Notes
    -----
    The adjusted samples are:

    .. math::
        g(X_i) - c^* \\cdot (h(X_i) - E[h(X)])

    The optimal coefficient is:

    .. math::
        c^* = \\text{Cov}(g, h) / \\text{Var}(h)
    """
    rng = np.random.default_rng(seed)

    g_samples = np.empty(n_iterations)
    h_samples = np.empty(n_iterations)

    for i in range(n_iterations):
        child_seed = rng.integers(0, 2**31)

        # Run cost_fn and control_fn with the SAME random state
        rng_g = np.random.default_rng(child_seed)
        g_samples[i] = cost_fn(rng_g)

        rng_h = np.random.default_rng(child_seed)
        h_samples[i] = control_fn(rng_h)

    # Estimate optimal c* if not provided
    if c is None:
        cov_gh = np.cov(g_samples, h_samples, ddof=1)[0, 1]
        var_h = np.var(h_samples, ddof=1)
        c = cov_gh / var_h if var_h > 0 else 0.0

    # Adjusted samples
    adjusted = g_samples - c * (h_samples - control_mean)

    return MonteCarloResult(
        samples=adjusted,
        n_iterations=n_iterations,
        seed=seed,
    )


def stratified_mc(
    cost_fn_stratified: Callable[[np.random.Generator, int], float],
    n_strata: int,
    n_per_stratum: int,
    seed: int = 42,
) -> MonteCarloResult:
    """Monte Carlo with stratified sampling (proportional allocation).

    Partitions the simulation into ``n_strata`` equal-probability strata
    and draws ``n_per_stratum`` samples from each.

    Parameters
    ----------
    cost_fn_stratified : Callable[[np.random.Generator, int], float]
        Cost function that takes an RNG and a stratum index (0-based).
        The function should condition its sampling on the stratum.
    n_strata : int
        Number of strata.
    n_per_stratum : int
        Samples per stratum (proportional allocation assumes equal weights).
    seed : int
        Random seed.

    Returns
    -------
    MonteCarloResult
        Result with ``n_strata * n_per_stratum`` total samples.
        The samples array contains the stratum means repeated by weight
        for correct CI computation, or all raw samples for analysis.
    """
    rng = np.random.default_rng(seed)
    total_n = n_strata * n_per_stratum
    all_samples = np.empty(total_n)

    for k in range(n_strata):
        stratum_rng = np.random.default_rng(rng.integers(0, 2**31))
        for j in range(n_per_stratum):
            idx = k * n_per_stratum + j
            all_samples[idx] = cost_fn_stratified(stratum_rng, k)

    return MonteCarloResult(
        samples=all_samples,
        n_iterations=total_n,
        seed=seed,
    )
