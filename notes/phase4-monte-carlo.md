# Phase 4 — The Monte Carlo Estimator

## Overview

Phases 1–3 built the mathematical toolkit: expected value, variance, LLN,
CLT, and confidence intervals. This phase ties everything together by
formalising the **Monte Carlo estimator** — the object at the centre of
every simulation we will run.

---

## 1. The Monte Carlo Estimator

### Setup

We want to estimate a quantity $\theta$ that can be expressed as an
expectation:

$$
\theta = E[g(X)]
$$

where $X$ is a random vector with a known distribution and $g$ is a
measurable function.

**In the budget model:** $X = (S_1, \ldots, S_n, H_1, \ldots, H_n, I, C_1, \ldots, C_I)$
is the vector of all random inputs, and $g(X) = X_{\text{total}}$ is the
total annual cost function.

### Definition

**Definition 1.1 (Monte Carlo Estimator).** Let $X_1, X_2, \ldots, X_N$ be
i.i.d. draws from the distribution of $X$. The **Monte Carlo estimator**
of $\theta = E[g(X)]$ is:

$$
\hat{\theta}_N = \frac{1}{N} \sum_{i=1}^N g(X_i)
$$

Each $g(X_i)$ is the result of one simulation — one "possible year" of the
budget. The estimator is simply the arithmetic mean of $N$ independent
simulations.

---

## 2. Properties of the Estimator

### Theorem 2.1 — Unbiasedness

**Statement.** $E[\hat{\theta}_N] = \theta$.

**Proof.** By linearity of expectation (Phase 1, Theorem 2.1):

$$
E[\hat{\theta}_N] = E\left[\frac{1}{N} \sum_{i=1}^N g(X_i)\right] = \frac{1}{N} \sum_{i=1}^N E[g(X_i)]
$$

Since $X_i$ are identically distributed, $E[g(X_i)] = E[g(X)] = \theta$ for
all $i$:

$$
= \frac{1}{N} \cdot N \cdot \theta = \theta \qquad \blacksquare
$$

**Interpretation.** The Monte Carlo estimator has no systematic bias — on
average, it hits the right answer. Individual runs may be above or below
$\theta$, but the errors cancel in expectation.

### Theorem 2.2 — Consistency (WLLN)

**Statement.** $\hat{\theta}_N \xrightarrow{P} \theta$ as $N \to \infty$.

**Proof.** The random variables $Y_i = g(X_i)$ are i.i.d. with
$E[Y_i] = \theta$ and $\text{Var}(Y_i) = \text{Var}(g(X)) = \sigma_g^2 < \infty$.

By the Weak Law of Large Numbers (Phase 2, Theorem 3.1):

$$
\bar{Y}_N = \frac{1}{N}\sum_{i=1}^N Y_i \xrightarrow{P} E[Y_i] = \theta
$$

Since $\hat{\theta}_N = \bar{Y}_N$:

$$
\hat{\theta}_N \xrightarrow{P} \theta \qquad \blacksquare
$$

By the Strong Law (Phase 2, Theorem 4.1), we also have almost sure convergence:
$\hat{\theta}_N \xrightarrow{a.s.} \theta$.

### Theorem 2.3 — Asymptotic Normality (CLT)

**Statement.** For large $N$:

$$
\frac{\hat{\theta}_N - \theta}{\sigma_g / \sqrt{N}} \;\dot{\sim}\; N(0, 1)
$$

**Proof.** Direct application of the CLT (Phase 3, Theorem 2.1) to the i.i.d.
sequence $Y_i = g(X_i)$. $\blacksquare$

**Consequence.** The $(1-\alpha)$ confidence interval for $\theta$ is:

$$
\hat{\theta}_N \pm z_{\alpha/2} \cdot \frac{s_N}{\sqrt{N}}
$$

where $s_N$ is the sample standard deviation of $g(X_1), \ldots, g(X_N)$.

---

## 3. Convergence Rate and the Dimension-Free Advantage

### Standard Error

$$
\text{SE}(\hat{\theta}_N) = \frac{\sigma_g}{\sqrt{N}}
$$

The error decays as $O(1/\sqrt{N})$, which means:

| To improve precision by | You need | Extra simulations |
|------------------------|----------|-------------------|
| 2× | 4× more $N$ | $3N$ additional |
| 10× | 100× more $N$ | $99N$ additional |
| 100× | 10,000× more $N$ | $9{,}999N$ additional |

### Mean Squared Error

**Theorem 3.1.** $\text{MSE}(\hat{\theta}_N) = \sigma_g^2 / N$.

**Proof.** By the bias-variance decomposition:

$$
\text{MSE}(\hat{\theta}_N) = \text{Bias}^2(\hat{\theta}_N) + \text{Var}(\hat{\theta}_N)
$$

Since the estimator is unbiased (Theorem 2.1), $\text{Bias} = 0$:

$$
\text{MSE}(\hat{\theta}_N) = \text{Var}(\hat{\theta}_N) = \frac{\sigma_g^2}{N} \qquad \blacksquare
$$

### Dimension-Free Property

The convergence rate $O(1/\sqrt{N})$ depends **only on $N$**, not on the
dimension of $X$. This is the key advantage of Monte Carlo over deterministic
numerical integration.

**Comparison with quadrature:**

| Method | Rate | Dimension dependence |
|--------|------|---------------------|
| Trapezoidal rule | $O(N^{-2/d})$ | Exponential in $d$ (curse of dimensionality) |
| Simpson's rule | $O(N^{-4/d})$ | Exponential in $d$ |
| Monte Carlo | $O(N^{-1/2})$ | **None** |

For our budget model, $X$ has dimension $d = n + 12n + 1 + I = 651+$
(50 salaries + 600 overtime values + 1 incident count + incident costs).
Any deterministic quadrature method would be completely impractical.

---

## 4. Implementation Design

### Architecture

```
src/model.py          → BudgetModel (configurable parameters, simulate_one_year)
src/monte_carlo.py    → MonteCarloSimulator (run N iterations, store results)
src/analysis.py       → compute_ci, prob_over_budget, summary_stats
```

### Reproducibility

Seed management is critical for scientific reproducibility:

- Each simulation run takes a `seed` parameter.
- The seed initialises a `numpy.random.Generator` via `default_rng(seed)`.
- The same seed always produces the same results.
- Different seeds produce independent results.

### Separation of Concerns

- **model.py** knows about budget structure but not about Monte Carlo.
- **monte_carlo.py** knows how to run simulations but not about budgets.
- **analysis.py** knows how to analyse arrays but not about models.

This makes each component independently testable and reusable.
