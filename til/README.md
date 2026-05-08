# TIL — Today I Learned

Short, portfolio-ready notes capturing one non-obvious insight from each phase
of the Monte Carlo Budget project. Each TIL is a **skeleton**: hook → insight
→ example → takeaway. The author writes the final text in their own voice.

## Why TILs?

The article publishes once. The TILs publish continuously — one per phase on
LinkedIn, the personal blog, or Medium. They keep the work visible while the
article matures, and each one is small enough to read on a phone during a
coffee break.

## Format

Each file:

- **Title** that states the insight, not the topic
- **100–300 words**
- **One concrete example** (numbers or a small matrix)
- **One-line takeaway**
- **Tags:** the phase, the math branch, the applied domain

## Index

| Phase | TIL file | Insight |
|-------|----------|---------|
| 1 | [til-phase-1-linearity-without-independence.md](til-phase-1-linearity-without-independence.md) | $E[\sum X_i] = \sum E[X_i]$ holds even when components are correlated |
| 2 | [til-phase-2-chebyshev-is-loose-by-design.md](til-phase-2-chebyshev-is-loose-by-design.md) | Why Chebyshev is conservative — and why that is a feature, not a bug |
| 3 | [til-phase-3-precision-is-quadratic.md](til-phase-3-precision-is-quadratic.md) | Halving the CI width quadruples the simulation cost |
| 4 | [til-phase-4-dimension-free-convergence.md](til-phase-4-dimension-free-convergence.md) | Monte Carlo's $O(1/\sqrt{N})$ rate does not depend on the input dimension |
| 5 | [til-phase-5-control-variate-as-leverage.md](til-phase-5-control-variate-as-leverage.md) | One known mean turns 50,000 simulations into 1,000 |
| 6 | [til-phase-6-fyf-is-bayesian-update.md](til-phase-6-fyf-is-bayesian-update.md) | Periodic forecast reviews are informal Bayesian updates |
| 7 | [til-phase-7-tornado-tells-you-where-to-spend.md](til-phase-7-tornado-tells-you-where-to-spend.md) | Sensitivity analysis is a tool for prioritising modelling effort |

## Publishing Order

Draft each TIL during the corresponding phase, polish after the phase PR is
merged, and publish in index order (1 → 7) on LinkedIn, Medium, or a
personal blog. Each post should link back to the article's GitHub repo so
the audience can follow the deeper material.
