"""Experiment F — Animated Convergence GIF for LinkedIn.

Generates ``figures/convergence.gif``: animated histogram forming as
simulation count increases, with running mean and CI band.

Also exports key frames as PNGs.

Usage:
    python scripts/gen_convergence_gif.py

Requires: pillow (for GIF export)
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

from src.model import BudgetModel
from src.monte_carlo import MonteCarloSimulator

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# --- Setup ---
model = BudgetModel()
E_analytical = model.analytical_expected_total()

# Run a large simulation
N_TOTAL = 10_000
SEED = 42
simulator = MonteCarloSimulator(
    cost_fn=lambda rng: model.simulate_one_year(rng).total_cost
)
result = simulator.run(n_iterations=N_TOTAL, seed=SEED)
all_samples = result.samples

# Frame checkpoints
FRAME_NS = [100, 200, 500, 1_000, 2_000, 5_000, 10_000]
Z_95 = 1.96

# --- Compute axis limits from full dataset ---
x_min = np.percentile(all_samples, 0.5) / 1e6
x_max = np.percentile(all_samples, 99.5) / 1e6
bins = np.linspace(x_min, x_max, 60)

# --- Create animation ---
fig, ax = plt.subplots(figsize=(10, 6))


def animate(frame_idx: int):
    ax.clear()
    n = FRAME_NS[frame_idx]
    samples = all_samples[:n]
    data_m = samples / 1e6

    # Histogram
    ax.hist(data_m, bins=bins, density=True, alpha=0.6,
            color="steelblue", edgecolor="white")

    # Running mean
    mean_val = samples.mean()
    ax.axvline(mean_val / 1e6, color="darkblue", ls="-", lw=2,
               label=f"Mean = R\\$ {mean_val/1e6:.2f}M")

    # Analytical mean
    ax.axvline(E_analytical / 1e6, color="red", ls="--", lw=1.5,
               label=f"Analytical = R\\$ {E_analytical/1e6:.2f}M")

    # 95% CI band for the mean
    se = samples.std(ddof=1) / np.sqrt(n) if n > 1 else 0
    ci_lo = (mean_val - Z_95 * se) / 1e6
    ci_hi = (mean_val + Z_95 * se) / 1e6
    ax.axvspan(ci_lo, ci_hi, alpha=0.2, color="green",
               label=f"95% CI: ±R\\$ {Z_95*se/1e3:.0f}K")

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, None)
    ax.set_xlabel("Total Annual Cost (R\\$ millions)")
    ax.set_ylabel("Density")
    ax.set_title(f"Monte Carlo Budget Simulation — N = {n:,}", fontsize=14)
    ax.legend(fontsize=9, loc="upper right")

    return ax


# Create animation
anim = animation.FuncAnimation(
    fig, animate, frames=len(FRAME_NS), interval=800, repeat=True
)

# Save GIF
anim.save("figures/convergence.gif", writer="pillow", fps=1.2, dpi=150)
print("Saved: figures/convergence.gif")

# --- Export key frames as PNGs ---
for i, n in enumerate(FRAME_NS):
    if n in [100, 1_000, 10_000]:
        fig_frame, ax_frame = plt.subplots(figsize=(10, 6))
        samples = all_samples[:n]
        data_m = samples / 1e6
        ax_frame.hist(data_m, bins=bins, density=True, alpha=0.6,
                      color="steelblue", edgecolor="white")
        mean_val = samples.mean()
        ax_frame.axvline(mean_val / 1e6, color="darkblue", ls="-", lw=2)
        ax_frame.axvline(E_analytical / 1e6, color="red", ls="--", lw=1.5)
        se = samples.std(ddof=1) / np.sqrt(n) if n > 1 else 0
        ci_lo = (mean_val - Z_95 * se) / 1e6
        ci_hi = (mean_val + Z_95 * se) / 1e6
        ax_frame.axvspan(ci_lo, ci_hi, alpha=0.2, color="green")
        ax_frame.set_xlim(x_min, x_max)
        ax_frame.set_xlabel("Total Annual Cost (R\\$ millions)")
        ax_frame.set_ylabel("Density")
        ax_frame.set_title(f"Monte Carlo Budget Simulation — N = {n:,}")
        plt.tight_layout()
        fname = f"figures/convergence_frame_n{n}.png"
        plt.savefig(fname, dpi=150, bbox_inches="tight")
        plt.close(fig_frame)
        print(f"Saved: {fname}")

plt.close(fig)
