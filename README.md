# Why Your Budget Never Hits the Exact Number

## Monte Carlo Simulation for Stochastic Budget Modelling — from Point Estimates to Probability Distributions

Point estimates ignore uncertainty. This project uses Monte Carlo simulation to
approximate the full distribution of budget outcomes, enabling interval-based
forecasts. Grounded in the Law of Large Numbers and Central Limit Theorem.
The framework is general; IT headcount planning serves as the primary case study.

## About

A **portfolio-grade technical article** that replaces traditional point-estimate
budgeting with stochastic modelling via Monte Carlo simulation. The article
derives the mathematical foundations from first principles and demonstrates the
approach on an IT headcount budget — one instantiation of a general template
that applies to any budget with proportional costs, fixed charges, and rare
disruptive events.

### What This Project Is

This is a **technical article for portfolio and personal development**, not
production software. The primary deliverable is a written article with rigorous
mathematical content, supported by correct and reproducible code.

## Project Structure

```
monte-carlo-budget-article/
├── article/              # Final article source (Markdown)
├── docs/                 # Planning documents (thesis, model spec, outline)
├── src/                  # Reusable source code (model, MC engine, analysis)
├── scripts/              # Standalone experiment and visualization scripts
├── notebooks/            # Jupyter notebooks (exploration)
├── exercises/            # Paper exercises (one file per phase)
├── figures/              # Generated plots and diagrams
├── notes/                # Phase-by-phase theory notes
├── tests/                # Unit tests (pytest)
└── pyproject.toml        # Project metadata, dependencies + ruff config
```

## Tech Stack

- Python 3.10+
- numpy / scipy — numerical computation and statistical distributions
- matplotlib / seaborn — publication-quality figures
- pandas — data manipulation
- ruff — linting
- pytest — testing

## Quick Start

```bash
# Clone the repository
git clone https://github.com/brunoramosmartins/monte-carlo-budget-article.git
cd monte-carlo-budget-article

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install project with all dependencies
pip install -e ".[dev,notebook]"

# Run linter
ruff check .

# Run tests
pytest tests/
```

## Roadmap

See [roadmap-monte-carlo-budget-v1.md](roadmap-monte-carlo-budget-v1.md) for the
full project roadmap with 10 phases, from mathematical foundations to publication.

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Foundation — thesis, model design, project scaffold | In Progress |
| Phase 1 | Probability Foundations | Planned |
| Phase 2 | Convergence Theorems (LLN) | Planned |
| Phase 3 | CLT & Confidence Intervals | Planned |
| Phase 4 | Monte Carlo Method | Planned |
| Phase 5 | Variance Reduction | Planned |
| Phase 6 | Bayesian Comparison | Planned |
| Phase 7 | Experiments & Visualizations | Planned |
| Phase 8 | Article Writing | Planned |
| Phase 9 | Review & Publish | Planned |

## License

MIT — see [LICENSE](LICENSE) for details.
