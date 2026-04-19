"""Experiment A — LLN Convergence (publication-quality).

Generates ``figures/lln_convergence.png``: 10 independent runs of the
sample mean of LogNormal salaries converging to E[S], with Chebyshev
95% confidence band overlay.

Usage:
    python scripts/exp_convergence.py
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)

# --- Parameters ---
MU_S, SIGMA_S = 9.2, 0.3
E_S = np.exp(MU_S + SIGMA_S**2 / 2)
VAR_S = (np.exp(SIGMA_S**2) - 1) * np.exp(2 * MU_S + SIGMA_S**2)
SD_S = np.sqrt(VAR_S)

N = 10_000
N_RUNS = 10
ALPHA = 0.05

n_vals = np.arange(1, N + 1)
chebyshev_hw = SD_S / np.sqrt(n_vals * ALPHA)

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6))

colors = plt.cm.tab10(np.linspace(0, 1, N_RUNS))
for i in range(N_RUNS):
    rng = np.random.default_rng(seed=100 + i)
    samples = rng.lognormal(mean=MU_S, sigma=SIGMA_S, size=N)
    running_mean = np.cumsum(samples) / n_vals
    ax.plot(n_vals, running_mean, color=colors[i], lw=0.5, alpha=0.7)

ax.axhline(E_S, color="red", ls="--", lw=2,
           label=f"$E[S]$ = R\\$ {E_S:,.0f}")
ax.fill_between(n_vals, E_S - chebyshev_hw, E_S + chebyshev_hw,
                alpha=0.12, color="orange",
                label="Chebyshev 95% band")

ax.set_xlabel("Number of samples $n$")
ax.set_ylabel("Running mean (R\\$)")
ax.set_title("Law of Large Numbers — Salary Convergence")
ax.legend(loc="upper right")
ax.set_xlim(1, N)
ax.set_ylim(E_S - 4000, E_S + 4000)

plt.tight_layout()
plt.savefig("figures/lln_convergence.png", dpi=300, bbox_inches="tight")
print("Saved: figures/lln_convergence.png")
