"""Experiment D — Variance Reduction Comparison (publication-quality).

Generates ``figures/variance_reduction_comparison.png``: CI width vs N
for naive MC, antithetic variates, and control variates.

Usage:
    python scripts/exp_variance_reduction.py
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.model import BudgetModel
from src.monte_carlo import MonteCarloSimulator
from src.analysis import compute_ci
from src.variance_reduction import antithetic_mc, control_variate_mc

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)

model = BudgetModel()
SEED = 42

cost_fn = lambda rng: model.simulate_one_year(rng).total_cost

def salary_control_fn(rng: np.random.Generator) -> float:
    result = model.simulate_one_year(rng)
    return result.salary_cost / (model.params.benefits_multiplier * 12)

E_salary_sum = model.params.n_employees * np.exp(
    model.params.mu_salary + model.params.sigma_salary**2 / 2
)

N_values = [500, 1_000, 2_000, 5_000, 10_000]
methods = {
    "Naive MC": {"widths": [], "color": "steelblue", "marker": "o"},
    "Antithetic": {"widths": [], "color": "coral", "marker": "s"},
    "Control Variate": {"widths": [], "color": "green", "marker": "^"},
}

for n in N_values:
    print(f"Running N = {n:,}...")

    # Naive
    r = MonteCarloSimulator(cost_fn).run(n, seed=SEED)
    ci = compute_ci(r.samples)
    methods["Naive MC"]["widths"].append((ci[1] - ci[0]) / 1e3)

    # Antithetic
    r = antithetic_mc(cost_fn, n_pairs=n // 2, seed=SEED)
    ci = compute_ci(r.samples)
    methods["Antithetic"]["widths"].append((ci[1] - ci[0]) / 1e3)

    # Control variate
    r = control_variate_mc(
        cost_fn=cost_fn,
        control_fn=salary_control_fn,
        control_mean=E_salary_sum,
        n_iterations=n,
        seed=SEED,
    )
    ci = compute_ci(r.samples)
    methods["Control Variate"]["widths"].append((ci[1] - ci[0]) / 1e3)

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))

for name, m in methods.items():
    ax.plot(N_values, m["widths"], marker=m["marker"], color=m["color"],
            lw=2, ms=8, label=name)

ax.set_xlabel("Number of simulations $N$")
ax.set_ylabel("95% CI width (R\\$ thousands)")
ax.set_title("Variance Reduction: CI Width vs Computational Budget")
ax.legend()
ax.set_xscale("log")
ax.set_yscale("log")

plt.tight_layout()
plt.savefig("figures/variance_reduction_comparison.png", dpi=300,
            bbox_inches="tight")
print("\nSaved: figures/variance_reduction_comparison.png")
