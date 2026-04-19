# Thesis — Why Your Budget Never Hits the Exact Number

## Central Claim (v0.1)

> A point-estimate budget is a single sample from an unknown distribution — it
> carries no information about its own uncertainty. Monte Carlo simulation
> recovers the full distribution, turning "we expect to spend R$ 12M" into
> "we are 90% confident spending will fall between R$ 11.2M and R$ 13.1M".
> The mathematical guarantee comes from the Law of Large Numbers (convergence
> of the estimator) and the Central Limit Theorem (quantification of the error).

## Central Axis

Every budget estimate is a random variable. Treating it as a constant discards
information.

```
Point estimate = E[X]  (a single number)
Monte Carlo    = F_X   (the full distribution)
```

## Scope

### What This Article Covers

1. **Probability foundations** — random variables, expected value, variance,
   covariance, key distributions (LogNormal, Poisson, Normal)
2. **Law of Large Numbers** — Markov's inequality, Chebyshev's inequality,
   Weak LLN (full proof), Strong LLN (statement + intuition)
3. **Central Limit Theorem** — MGF approach proof, Berry-Esseen bound,
   confidence intervals for Monte Carlo estimators
4. **Monte Carlo method** — formal estimator, unbiasedness, consistency,
   convergence rate $O(1/\sqrt{N})$, implementation
5. **Variance reduction** — antithetic variates, control variates, stratified
   sampling (derivations + implementation)
6. **Bayesian comparison** — brief conceptual overview, frequentist vs
   Bayesian framing of budget estimation
7. **Applied IT budget model** — generic headcount budget with salaries,
   benefits, overtime, and incidents as stochastic components

### Anti-Scope (What This Article Does NOT Cover)

- Time-series forecasting (ARIMA, Prophet, etc.)
- Real company data or proprietary information
- Production deployment or MLOps
- Deep Bayesian treatment (MCMC, variational inference)
- Multi-year budget models or inflation dynamics
- Correlation modelling between cost components (mentioned as expansion)

## Target Audience

- Data scientists and analysts working with financial planning
- Finance-adjacent tech roles (Analytics Engineers, BI developers)
- Statisticians interested in applied simulation
- Anyone who wants to understand why spreadsheet budgets are inherently limited

### Prerequisite Knowledge

- Calculus (integration, Taylor series)
- Basic probability (what a random variable is, informally)
- Python familiarity (for code examples)

## Abstract

Traditional IT budget planning relies on point estimates — single numbers that
carry no information about their own uncertainty. When the CFO asks "what will
we spend next year on headcount?", the answer is typically a deterministic
calculation: headcount times average salary times benefits multiplier. This
article argues that every component of that calculation is a random variable,
and treating them as constants discards critical information. Using Monte Carlo
simulation grounded in the Law of Large Numbers and Central Limit Theorem, we
replace the single number with a probability distribution of outcomes. The
result: not just "R$ 12M" but "90% confidence the budget falls between
R$ 11.2M and R$ 13.1M, with a 7% probability of exceeding the ceiling." We
derive the mathematical foundations from first principles, implement the
simulation in Python, apply variance reduction techniques for efficiency, and
demonstrate the approach on a generic IT headcount budget model.
