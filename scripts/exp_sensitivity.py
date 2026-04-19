"""Experiment E — Sensitivity Analysis and Tornado Chart.

Generates ``figures/sensitivity_tornado.png``: horizontal bar chart
ranking parameters by their impact on E[X_total] when varied ±20%.

Usage:
    python scripts/exp_sensitivity.py
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.model import BudgetModel, BudgetModelParams
from src.monte_carlo import MonteCarloSimulator

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

N_SIM = 10_000
SEED = 42
VARIATION = 0.20  # ±20%

# --- Base case ---
base_model = BudgetModel()
base_sim = MonteCarloSimulator(
    cost_fn=lambda rng: base_model.simulate_one_year(rng).total_cost
)
base_result = base_sim.run(N_SIM, seed=SEED)
base_mean = base_result.mean

print(f"Base case E[X] = R$ {base_mean:,.0f}")
print()

# --- Parameters to vary ---
params_to_vary = [
    ("mu_salary", "μ_s (salary log-mean)"),
    ("sigma_salary", "σ_s (salary log-std)"),
    ("benefits_multiplier", "β (benefits multiplier)"),
    ("n_employees", "n (headcount)"),
    ("lambda_overtime", "λ_h (overtime rate)"),
    ("overtime_hourly_rate", "r_ot (overtime $/hr)"),
    ("lambda_incidents", "λ_I (incident rate)"),
    ("mu_incident_cost", "μ_I (incident cost log-mean)"),
]

results = []

for param_name, label in params_to_vary:
    base_val = getattr(BudgetModelParams(), param_name)

    for direction, factor in [("low", 1 - VARIATION), ("high", 1 + VARIATION)]:
        new_val = base_val * factor
        if param_name == "n_employees":
            new_val = int(round(new_val))

        kwargs = {param_name: new_val}
        params = BudgetModelParams(**kwargs)
        model = BudgetModel(params)
        sim = MonteCarloSimulator(
            cost_fn=lambda rng, m=model: m.simulate_one_year(rng).total_cost
        )
        r = sim.run(N_SIM, seed=SEED)

        delta = r.mean - base_mean
        delta_pct = delta / base_mean * 100

        results.append({
            "param": param_name,
            "label": label,
            "direction": direction,
            "new_val": new_val,
            "mean": r.mean,
            "delta": delta,
            "delta_pct": delta_pct,
        })

# --- Print results ---
print(f"{'Parameter':<30} {'Direction':<6} {'E[X]':>14} {'ΔE[X]':>14} {'Δ%':>8}")
print("-" * 76)
for r in results:
    print(f"{r['label']:<30} {r['direction']:<6} "
          f"{r['mean']:>14,.0f} {r['delta']:>14,.0f} {r['delta_pct']:>7.2f}%")

# --- Tornado chart ---
# Compute range (high - low) for each parameter
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

# Low bars (left of zero)
ax.barh(y_pos, low_deltas, height=0.6, color="steelblue", alpha=0.8,
        label="−20%")
# High bars (right of zero)
ax.barh(y_pos, high_deltas, height=0.6, color="coral", alpha=0.8,
        label="+20%")

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel("Change in $E[X_{total}]$ (%)")
ax.set_title("Sensitivity Analysis — Tornado Chart (±20% variation)")
ax.axvline(0, color="black", lw=0.8)
ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig("figures/sensitivity_tornado.png", dpi=300, bbox_inches="tight")
print(f"\nSaved: figures/sensitivity_tornado.png")
