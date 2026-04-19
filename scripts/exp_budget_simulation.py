"""Experiment C — Full Budget Simulation (publication-quality).

Generates ``figures/budget_simulation.png``: dual-panel figure with
histogram + CDF, annotated with mean, median, P5/P95, budget ceiling,
and P(overbudget).

Usage:
    python scripts/exp_budget_simulation.py
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

from src.model import BudgetModel
from src.monte_carlo import MonteCarloSimulator
from src.analysis import compute_ci, prob_over_budget, summary_stats

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# --- Setup ---
model = BudgetModel()
simulator = MonteCarloSimulator(
    cost_fn=lambda rng: model.simulate_one_year(rng).total_cost
)

N = 50_000
SEED = 42
BUDGET_CEILING = 12_500_000

result = simulator.run(n_iterations=N, seed=SEED)
ss = summary_stats(result.samples)
ci = compute_ci(result.samples, alpha=0.05)
p_over = prob_over_budget(result.samples, BUDGET_CEILING)
E_analytical = model.analytical_expected_total()

print("=== Budget Simulation Results ===")
print(f"N = {N:,}")
print(f"Mean      = R$ {ss['mean']:>14,.2f}")
print(f"Median    = R$ {ss['median']:>14,.2f}")
print(f"SD        = R$ {ss['std']:>14,.2f}")
print(f"SE        = R$ {ss['se']:>14,.2f}")
print(f"P5        = R$ {ss['p5']:>14,.2f}")
print(f"P95       = R$ {ss['p95']:>14,.2f}")
print(f"95% CI    = [R$ {ci[0]:,.0f}, R$ {ci[1]:,.0f}]")
print(f"Analytical E[X] = R$ {E_analytical:>14,.2f}")
print(f"P(X > {BUDGET_CEILING/1e6:.1f}M) = {p_over:.2%}")

# --- Dual figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
data_m = result.samples / 1e6

# Panel 1: Histogram
ax1.hist(data_m, bins=100, density=True, alpha=0.6,
         color="steelblue", edgecolor="white", label="Simulated costs")
ax1.axvline(ss["mean"] / 1e6, color="darkblue", ls="-", lw=2,
            label=f"Mean = R\\$ {ss['mean']/1e6:.2f}M")
ax1.axvline(ss["median"] / 1e6, color="green", ls="-.", lw=1.5,
            label=f"Median = R\\$ {ss['median']/1e6:.2f}M")
ax1.axvline(ss["p5"] / 1e6, color="orange", ls="--", lw=1.5,
            label=f"P5 = R\\$ {ss['p5']/1e6:.2f}M")
ax1.axvline(ss["p95"] / 1e6, color="orange", ls="--", lw=1.5,
            label=f"P95 = R\\$ {ss['p95']/1e6:.2f}M")
ax1.axvline(BUDGET_CEILING / 1e6, color="darkred", ls=":", lw=2,
            label=f"Ceiling R\\$ {BUDGET_CEILING/1e6:.1f}M "
                  f"(P(over)={p_over:.1%})")

ax1.set_xlabel("Total Annual Cost (R\\$ millions)")
ax1.set_ylabel("Density")
ax1.set_title("Budget Cost Distribution")
ax1.legend(fontsize=8, loc="upper right")

# Panel 2: CDF
sorted_data = np.sort(data_m)
cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

ax2.plot(sorted_data, cdf, color="steelblue", lw=1.5)
ax2.axvline(ss["mean"] / 1e6, color="darkblue", ls="-", lw=1.5,
            label=f"Mean")
ax2.axhline(0.5, color="gray", ls=":", lw=0.8, alpha=0.5)
ax2.axvline(BUDGET_CEILING / 1e6, color="darkred", ls=":", lw=2,
            label=f"Ceiling")
ax2.axhline(1 - p_over, color="darkred", ls="--", lw=1, alpha=0.5)
ax2.annotate(f"P(X ≤ ceiling) = {1 - p_over:.1%}",
             xy=(BUDGET_CEILING / 1e6, 1 - p_over),
             xytext=(BUDGET_CEILING / 1e6 + 0.2, 1 - p_over - 0.08),
             fontsize=9, color="darkred",
             arrowprops=dict(arrowstyle="->", color="darkred"))

ax2.set_xlabel("Total Annual Cost (R\\$ millions)")
ax2.set_ylabel("Cumulative Probability")
ax2.set_title("Cumulative Distribution Function")
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig("figures/budget_simulation.png", dpi=300, bbox_inches="tight")
print("\nSaved: figures/budget_simulation.png")
