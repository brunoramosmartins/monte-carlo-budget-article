# Why Your Budget Never Hits the Exact Number

**Monte Carlo Simulation for Stochastic Budget Modelling — from Point Estimates to Probability Distributions**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Abstract

Traditional budget planning relies on point estimates — single numbers that
carry no information about their own uncertainty. This project replaces the
single number with a **probability distribution** using Monte Carlo simulation,
grounded in the Law of Large Numbers and Central Limit Theorem.

The result: not just "R$ 12M" but **"we are 90% confident spending will fall
between R$ 11.2M and R$ 13.1M, with a 7% probability of exceeding the ceiling."**

The framework is **general** — it applies to any budget decomposable into
stochastic components (headcount, projects, cloud infrastructure, procurement,
marketing). An IT headcount budget serves as the concrete case study.

## Key Results

| Metric | Value |
|--------|-------|
| Analytical E[X] vs MC mean | Within 0.1% |
| 95% CI half-width (N=50K) | ~R$ 4K |
| Best variance reduction | Control variates (~10-50x) |
| Most sensitive parameter | Dominant cost component's mean |

## Mathematical Content

The article derives everything from first principles:

1. **Probability Foundations** — Random variables, expected value, variance, covariance. LogNormal and Poisson moments derived via MGF.
2. **Law of Large Numbers** — Markov → Chebyshev → Weak LLN (complete proof chain). The MC estimator converges.
3. **Central Limit Theorem** — MGF proof with explicit Taylor expansion. Confidence intervals and minimum-N formula derived.
4. **Monte Carlo Estimator** — Unbiasedness, consistency, asymptotic normality proved. Dimension-free convergence rate.
5. **Variance Reduction** — Antithetic variates, control variates (optimal c* derived), stratified sampling. All with proofs.
6. **Bayesian Comparison** — Frequentist MC vs Bayesian framing, when each is appropriate.

## Project Structure

```
monte-carlo-budget-article/
├── article/                    # Final article (EN + PT-BR)
│   ├── monte-carlo-budget.md
│   └── monte-carlo-budget-pt.md
├── src/                        # Reusable source code
│   ├── model.py                # Budget cost model (configurable)
│   ├── monte_carlo.py          # Monte Carlo simulation engine
│   ├── analysis.py             # CI, P(overbudget), summary stats
│   └── variance_reduction.py   # Antithetic, control variates, stratified
├── scripts/                    # Standalone experiment scripts
│   ├── exp_convergence.py      # LLN convergence demo
│   ├── exp_clt_normality.py    # CLT normality emergence
│   ├── exp_budget_simulation.py # Full budget MC (50K iterations)
│   ├── exp_variance_reduction.py # Method comparison
│   ├── exp_sensitivity.py      # Tornado chart (±20% variation)
│   └── gen_convergence_gif.py  # Animated GIF for social media
├── notebooks/                  # Interactive exploration (Jupyter)
│   ├── 01_probability_foundations.ipynb
│   ├── 02_lln_convergence.ipynb
│   ├── 03_clt_confidence.ipynb
│   ├── 04_monte_carlo_core.ipynb
│   ├── 05_variance_reduction.ipynb
│   └── 06_budget_simulation.ipynb
├── notes/                      # Phase-by-phase theory notes
├── exercises/                  # Paper exercises (proofs + computations)
├── tests/                      # Unit tests (pytest)
├── docs/                       # Planning docs (thesis, model spec, outline)
├── figures/                    # Generated plots and GIF
└── pyproject.toml              # Dependencies + ruff config
```

## Quick Start

```bash
# Clone
git clone https://github.com/brunoramosmartins/monte-carlo-budget-article.git
cd monte-carlo-budget-article

# Setup
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

pip install -e ".[dev,notebook]"

# Run tests
pytest tests/

# Generate all figures
python scripts/exp_convergence.py
python scripts/exp_clt_normality.py
python scripts/exp_budget_simulation.py
python scripts/exp_variance_reduction.py
python scripts/exp_sensitivity.py
python scripts/gen_convergence_gif.py
```

## The Budget Model

Any budget with uncertain components follows the template:

$$
X_{\text{total}} = \underbrace{\sum_{i} f(Z_i)}_{\text{proportional costs}} + \underbrace{\text{fixed}}_{\text{deterministic}} + \underbrace{\sum_{j=1}^{N_{\text{events}}} C_j}_{\text{rare events}}
$$

The IT headcount instantiation uses LogNormal salaries, Poisson overtime, and compound Poisson incidents. See `docs/model-design.md` for the full specification and how to adapt the template to other domains.

## Exercises

Each phase includes paper exercises (proofs + computations) in `exercises/`:

| File | Topics |
|------|--------|
| `ex01_probability_foundations.md` | LogNormal MGF, variance of sums, Jensen's inequality |
| `ex02_convergence.md` | Markov, Chebyshev, WLLN proofs, minimum N via Chebyshev |
| `ex03_clt.md` | Normal MGF, CLT proof, CI derivation, Berry-Esseen |
| `ex04_monte_carlo.md` | Unbiasedness, consistency, MSE, scaling law |
| `ex05_variance_reduction.md` | Optimal c*, antithetic variance, stratified ≤ naive |

## Tech Stack

- **Python 3.10+** with type hints
- **numpy / scipy** — numerical computation and statistical distributions
- **matplotlib / seaborn** — publication-quality figures
- **pandas** — data manipulation
- **pytest** — 39+ unit tests
- **ruff** — linting (line-length=88, py310)

## References

1. Casella, G. & Berger, R. (2002). *Statistical Inference*. Duxbury.
2. Robert, C. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
3. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
4. Gelman, A. et al. (2013). *Bayesian Data Analysis*. CRC Press.

## License

MIT — see [LICENSE](LICENSE) for details.
