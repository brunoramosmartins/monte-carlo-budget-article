"""Experiment E — Sensitivity Analysis and Tornado Chart.

Generates ``figures/sensitivity_tornado.png``: horizontal bar chart
ranking parameters by their impact on E[X_total] when each parameter's
**effective contribution** is varied by ±20%.

Why effective contribution and not the raw parameter?
    For LogNormal-type parameters (mu_salary, mu_incident_cost), varying
    the raw mu by ±20% produces an exponential change in E[component]
    (E[S] = exp(mu + sigma^2/2)) — the chart becomes dominated by these
    parameters not because they are most sensitive in a business sense,
    but because the parameter scale is logarithmic. The fairer comparison
    is to vary the *effective expected value* of each component by ±20%
    and see which component drives the total most.

Usage:
    python scripts/exp_sensitivity.py
"""

from dataclasses import replace

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.model import BudgetModel, BudgetModelParams
from src.monte_carlo import MonteCarloSimulator

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

N_SIM = 10_000
SEED = 42
VARIATION = 0.20  # ±20% on effective value

# --- Base case ---
base_params = BudgetModelParams()
base_model = BudgetModel(base_params)
base_sim = MonteCarloSimulator(
    cost_fn=lambda rng: base_model.simulate_one_year(rng).total_cost
)
base_result = base_sim.run(N_SIM, seed=SEED)
base_mean = base_result.mean

print(f"Base case E[X] = R$ {base_mean:,.0f}\n")


def perturb(params: BudgetModelParams, key: str, factor: float) -> BudgetModelParams:
    """Return a new params object with key perturbed so that the *effective*
    expected contribution of that parameter is multiplied by `factor`.

    For log-mean parameters (mu_salary, mu_incident_cost): adjusting by
    ln(factor) shifts E[exp(mu + sigma^2/2)] by exactly `factor`.

    For all other parameters (linear in E[X_total]): scale directly.
    """
    if key == "mu_salary":
        return replace(params, mu_salary=params.mu_salary + np.log(factor))
    if key == "mu_incident_cost":
        return replace(
            params, mu_incident_cost=params.mu_incident_cost + np.log(factor)
        )
    if key == "n_employees":
        new_n = int(round(params.n_employees * factor))
        return replace(params, n_employees=new_n)
    # Linear parameters: benefits_multiplier, lambda_overtime,
    # overtime_hourly_rate, lambda_incidents, sigma_salary
    current = getattr(params, key)
    return replace(params, **{key: current * factor})


# --- Parameters to vary (effective ±20%) ---
# Label includes "effective ±20%" reminder so chart reading is unambiguous
params_to_vary = [
    ("mu_salary", "μ_s (E[S])"),
    ("sigma_salary", "σ_s"),
    ("benefits_multiplier", "β (benefits)"),
    ("n_employees", "n (headcount)"),
    ("lambda_overtime", "λ_h (overtime rate)"),
    ("overtime_hourly_rate", "r_ot (overtime $/hr)"),
    ("lambda_incidents", "λ_I (incident rate)"),
    ("mu_incident_cost", "μ_I (E[C])"),
]

results = []

for key, label in params_to_vary:
    for direction, factor in [("low", 1 - VARIATION), ("high", 1 + VARIATION)]:
        new_params = perturb(base_params, key, factor)
        model = BudgetModel(new_params)
        sim = MonteCarloSimulator(
            cost_fn=lambda rng, m=model: m.simulate_one_year(rng).total_cost
        )
        r = sim.run(N_SIM, seed=SEED)

        delta = r.mean - base_mean
        delta_pct = delta / base_mean * 100

        results.append(
            {
                "key": key,
                "label": label,
                "direction": direction,
                "mean": r.mean,
                "delta": delta,
                "delta_pct": delta_pct,
            }
        )

# --- Print results ---
print(f"{'Parameter':<28} {'Direction':<6} {'E[X]':>14} {'ΔE[X]':>14} {'Δ%':>8}")
print("-" * 74)
for r in results:
    print(
        f"{r['label']:<28} {r['direction']:<6} "
        f"{r['mean']:>14,.0f} {r['delta']:>14,.0f} {r['delta_pct']:>7.2f}%"
    )

# --- Tornado chart ---
param_ranges = {}
for r in results:
    key = r["label"]
    if key not in param_ranges:
        param_ranges[key] = {"low_delta": 0, "high_delta": 0}
    if r["direction"] == "low":
        param_ranges[key]["low_delta"] = r["delta_pct"]
    else:
        param_ranges[key]["high_delta"] = r["delta_pct"]

# Sort by total range
sorted_params = sorted(
    param_ranges.items(),
    key=lambda x: abs(x[1]["high_delta"] - x[1]["low_delta"]),
)

labels = [p[0] for p in sorted_params]
low_deltas = [p[1]["low_delta"] for p in sorted_params]
high_deltas = [p[1]["high_delta"] for p in sorted_params]

fig, ax = plt.subplots(figsize=(10, 7))
y_pos = np.arange(len(labels))

ax.barh(
    y_pos, low_deltas, height=0.6, color="steelblue", alpha=0.8,
    label=r"Effective $-20\%$",
)
ax.barh(
    y_pos, high_deltas, height=0.6, color="coral", alpha=0.8,
    label=r"Effective $+20\%$",
)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel("Change in $E[X_{total}]$ (%)")
ax.set_title("Sensitivity Analysis — Tornado Chart (effective ±20%)")
ax.axvline(0, color="black", lw=0.8)
ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig("figures/sensitivity_tornado.png", dpi=300, bbox_inches="tight")
print(f"\nSaved: figures/sensitivity_tornado.png")
