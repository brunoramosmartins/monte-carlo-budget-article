"""Experiment B — CLT Normality Emergence (publication-quality).

Generates:
- ``figures/clt_normality_emergence.png``: histograms for n=1,5,10,30,100
- ``figures/clt_qq_plot.png``: QQ-plots for n=5,10,30,100

Usage:
    python scripts/exp_clt_normality.py
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

MU_S, SIGMA_S = 9.2, 0.3
E_S = np.exp(MU_S + SIGMA_S**2 / 2)
VAR_S = (np.exp(SIGMA_S**2) - 1) * np.exp(2 * MU_S + SIGMA_S**2)
SD_S = np.sqrt(VAR_S)

N_REP = 10_000
rng = np.random.default_rng(42)
x_grid = np.linspace(-4, 4, 200)
standard_normal_pdf = stats.norm.pdf(x_grid)

# --- Histograms ---
n_values = [1, 5, 10, 30, 100]
fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=True)

for ax, n in zip(axes, n_values):
    samples = rng.lognormal(mean=MU_S, sigma=SIGMA_S, size=(N_REP, n))
    sample_means = samples.mean(axis=1)
    z_scores = np.sqrt(n) * (sample_means - E_S) / SD_S

    ax.hist(z_scores, bins=50, density=True, alpha=0.6,
            color="steelblue", edgecolor="white")
    ax.plot(x_grid, standard_normal_pdf, "r-", lw=2, label="$N(0,1)$")
    ax.set_title(f"$n = {n}$")
    ax.set_xlim(-4, 4)
    ax.set_xlabel("$Z_n$")
    if n == 1:
        ax.set_ylabel("Density")
    ax.legend(fontsize=8)

fig.suptitle("CLT: Standardised Mean of LogNormal Salaries",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("figures/clt_normality_emergence.png", dpi=300, bbox_inches="tight")
print("Saved: figures/clt_normality_emergence.png")

# --- QQ-plots ---
qq_n_values = [5, 10, 30, 100]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, n in zip(axes, qq_n_values):
    samples = rng.lognormal(mean=MU_S, sigma=SIGMA_S, size=(N_REP, n))
    sample_means = samples.mean(axis=1)
    z_scores = np.sqrt(n) * (sample_means - E_S) / SD_S

    (osm, osr), (slope, intercept, r) = stats.probplot(z_scores, dist="norm")
    ax.scatter(osm, osr, s=2, alpha=0.3, color="steelblue")
    ax.plot(osm, slope * osm + intercept, "r-", lw=1.5)
    ax.set_title(f"$n = {n}$  ($R^2 = {r**2:.4f}$)")
    ax.set_xlabel("Theoretical Quantiles")
    if n == qq_n_values[0]:
        ax.set_ylabel("Empirical Quantiles")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

fig.suptitle("QQ-Plots: Standardised Mean vs $N(0,1)$", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig("figures/clt_qq_plot.png", dpi=300, bbox_inches="tight")
print("Saved: figures/clt_qq_plot.png")
