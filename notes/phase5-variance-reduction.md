# Phase 5 — Variance Reduction Techniques

## Overview

The naive Monte Carlo estimator has standard error $\text{SE} = \sigma_g / \sqrt{N}$.
To halve the CI width, we need $4\times$ more simulations. Variance reduction
techniques achieve tighter CIs **for the same $N$** by exploiting structure
in the problem.

Three techniques are derived and proved: antithetic variates, control variates,
and stratified sampling.

---

## 1. Antithetic Variates

### Idea

Instead of drawing $N$ independent samples, draw $N/2$ pairs $(X_i, X_i')$
where $X_i'$ is the "antithetic" (mirror) of $X_i$. If $g$ is monotone,
the pair $(g(X_i), g(X_i'))$ will be negatively correlated, reducing the
variance of their average.

### Construction

For a uniform random variable $U \sim \text{Uniform}(0, 1)$, the antithetic
partner is $U' = 1 - U$. For any distribution with CDF $F$:

$$
X = F^{-1}(U), \qquad X' = F^{-1}(1 - U)
$$

Since $U$ and $1 - U$ have the same Uniform(0,1) distribution, $X$ and $X'$
have the same marginal distribution. But they are **negatively correlated**
when $F^{-1}$ is monotone (which it always is).

### The Antithetic Estimator

**Definition.** The antithetic variate estimator is:

$$
\hat{\mu}_{AV} = \frac{1}{N/2} \sum_{i=1}^{N/2} \frac{g(X_i) + g(X_i')}{2}
$$

where $(X_i, X_i')$ are antithetic pairs. This uses $N$ function evaluations
total ($N/2$ pairs).

### Theorem 1.1 — Variance of the Antithetic Estimator

**Statement.**

$$
\text{Var}(\hat{\mu}_{AV}) = \frac{1}{2N}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right]
$$

**Proof.** Define $Y_i = \frac{g(X_i) + g(X_i')}{2}$. The pairs $(Y_1, \ldots, Y_{N/2})$
are i.i.d. (each pair is drawn independently), so:

$$
\text{Var}(\hat{\mu}_{AV}) = \text{Var}\left(\frac{1}{N/2}\sum_{i=1}^{N/2} Y_i\right) = \frac{\text{Var}(Y_i)}{N/2}
$$

Now compute $\text{Var}(Y_i)$:

$$
\text{Var}(Y_i) = \text{Var}\left(\frac{g(X) + g(X')}{2}\right)
$$

$$
= \frac{1}{4}\left[\text{Var}(g(X)) + \text{Var}(g(X')) + 2\,\text{Cov}(g(X), g(X'))\right]
$$

Since $X$ and $X'$ have the same distribution, $\text{Var}(g(X)) = \text{Var}(g(X'))$:

$$
= \frac{1}{4}\left[2\,\text{Var}(g(X)) + 2\,\text{Cov}(g(X), g(X'))\right]
$$

$$
= \frac{1}{2}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right]
$$

Substituting:

$$
\text{Var}(\hat{\mu}_{AV}) = \frac{1}{N/2} \cdot \frac{1}{2}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right]
$$

$$
= \frac{1}{N}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right] \cdot \frac{1}{2} \cdot \frac{2}{1}
$$

Wait, let me redo this carefully:

$$
\text{Var}(\hat{\mu}_{AV}) = \frac{\text{Var}(Y_i)}{N/2} = \frac{1}{N/2} \cdot \frac{1}{2}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right]
$$

$$
= \frac{1}{N}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right] \qquad \blacksquare
$$

### When Does It Help?

**Comparison with naive MC** (which has variance $\text{Var}(g(X))/N$):

$$
\text{Var}(\hat{\mu}_{AV}) \leq \text{Var}(\hat{\mu}_{MC}) \iff \text{Cov}(g(X), g(X')) \leq 0
$$

This holds when $g$ is a **monotone function** of $X$ and $X'$ is constructed
via the antithetic transformation. Since the budget total cost is an increasing
function of salaries and overtime, we expect negative covariance and thus
variance reduction.

---

## 2. Control Variates

### Idea

If we know $E[h(X)]$ analytically for some function $h$, we can use the
discrepancy $\bar{h}_N - E[h(X)]$ to correct our estimate of $E[g(X)]$.

### The Control Variate Estimator

**Definition.** For a coefficient $c \in \mathbb{R}$:

$$
\hat{\mu}_{CV} = \hat{\mu}_N - c\left(\bar{h}_N - E[h(X)]\right)
$$

where $\hat{\mu}_N = \frac{1}{N}\sum g(X_i)$ and $\bar{h}_N = \frac{1}{N}\sum h(X_i)$.

**Unbiasedness.** $E[\hat{\mu}_{CV}] = E[\hat{\mu}_N] - c(E[\bar{h}_N] - E[h(X)]) = \theta - c \cdot 0 = \theta$.

### Theorem 2.1 — Variance of the Control Variate Estimator

**Statement.**

$$
\text{Var}(\hat{\mu}_{CV}) = \frac{1}{N}\left[\text{Var}(g(X)) - 2c\,\text{Cov}(g(X), h(X)) + c^2\,\text{Var}(h(X))\right]
$$

**Proof.** Since $\hat{\mu}_{CV} = \frac{1}{N}\sum [g(X_i) - c \cdot h(X_i)] + c \cdot E[h(X)]$,
and the constant $c \cdot E[h(X)]$ does not affect variance:

$$
\text{Var}(\hat{\mu}_{CV}) = \text{Var}\left(\frac{1}{N}\sum [g(X_i) - c \cdot h(X_i)]\right)
$$

$$
= \frac{1}{N}\text{Var}(g(X) - c \cdot h(X))
$$

$$
= \frac{1}{N}\left[\text{Var}(g(X)) - 2c\,\text{Cov}(g(X), h(X)) + c^2\,\text{Var}(h(X))\right] \qquad \blacksquare
$$

### Theorem 2.2 — Optimal Coefficient

**Statement.** The variance-minimising coefficient is:

$$
c^* = \frac{\text{Cov}(g(X), h(X))}{\text{Var}(h(X))}
$$

**Proof.** The variance is a quadratic function of $c$. Taking the derivative
and setting it to zero:

$$
\frac{d}{dc}\text{Var}(\hat{\mu}_{CV}) = \frac{1}{N}\left[-2\,\text{Cov}(g, h) + 2c\,\text{Var}(h)\right] = 0
$$

$$
c^* = \frac{\text{Cov}(g, h)}{\text{Var}(h)}
$$

The second derivative is $\frac{2\,\text{Var}(h)}{N} > 0$, confirming this is
a minimum. $\blacksquare$

### Theorem 2.3 — Variance at Optimal $c^*$

**Statement.**

$$
\text{Var}(\hat{\mu}_{CV}^*) = \frac{\text{Var}(g(X))}{N}\left(1 - \rho_{g,h}^2\right)
$$

where $\rho_{g,h} = \text{Corr}(g(X), h(X))$.

**Proof.** Substitute $c^*$ into the variance formula:

$$
\text{Var}(\hat{\mu}_{CV}^*) = \frac{1}{N}\left[\text{Var}(g) - 2 \cdot \frac{\text{Cov}(g,h)}{\text{Var}(h)} \cdot \text{Cov}(g,h) + \frac{\text{Cov}(g,h)^2}{\text{Var}(h)^2} \cdot \text{Var}(h)\right]
$$

$$
= \frac{1}{N}\left[\text{Var}(g) - 2\frac{\text{Cov}(g,h)^2}{\text{Var}(h)} + \frac{\text{Cov}(g,h)^2}{\text{Var}(h)}\right]
$$

$$
= \frac{1}{N}\left[\text{Var}(g) - \frac{\text{Cov}(g,h)^2}{\text{Var}(h)}\right]
$$

$$
= \frac{\text{Var}(g)}{N}\left[1 - \frac{\text{Cov}(g,h)^2}{\text{Var}(g)\,\text{Var}(h)}\right]
$$

$$
= \frac{\text{Var}(g)}{N}\left(1 - \rho_{g,h}^2\right) \qquad \blacksquare
$$

**Interpretation.** The variance reduction factor is $(1 - \rho^2)$. If $h$
is highly correlated with $g$ (e.g., $|\rho| = 0.95$), then variance is
reduced by a factor of $1 - 0.9025 = 0.0975$ — roughly a $10\times$ improvement.

### Application to the Budget Model

The control variate is $h(X) = \sum_{i=1}^n S_i$ (total raw salaries). We know:

$$
E[h(X)] = n \cdot E[S_i] = 50 \times e^{9.245} \approx 518{,}101
$$

Since salaries dominate the total cost (~97%), we expect
$\rho_{g,h} \approx 0.95$, giving a variance reduction of ~10×.

---

## 3. Stratified Sampling

### Idea

Partition the sample space into $K$ non-overlapping strata $A_1, \ldots, A_K$
with $P(X \in A_k) = p_k$. Sample $n_k$ observations from each stratum
(where $\sum n_k = N$) and combine:

$$
\hat{\mu}_{SS} = \sum_{k=1}^K p_k \cdot \bar{g}_k
$$

where $\bar{g}_k$ is the sample mean within stratum $k$.

### Theorem 3.1 — Variance Reduction by Stratification

**Statement.** With proportional allocation ($n_k = N \cdot p_k$):

$$
\text{Var}(\hat{\mu}_{SS}) = \frac{1}{N}\sum_{k=1}^K p_k \, \sigma_k^2
$$

where $\sigma_k^2 = \text{Var}(g(X) \mid X \in A_k)$.

**Comparison.** The naive MC variance is:

$$
\text{Var}(\hat{\mu}_{MC}) = \frac{\sigma^2}{N} = \frac{1}{N}\left[\sum_k p_k \sigma_k^2 + \sum_k p_k(\mu_k - \mu)^2\right]
$$

by the **law of total variance**:

$$
\text{Var}(g(X)) = \underbrace{E[\text{Var}(g(X)|A)]}_{\sum p_k \sigma_k^2} + \underbrace{\text{Var}(E[g(X)|A])}_{\sum p_k(\mu_k - \mu)^2}
$$

Therefore:

$$
\text{Var}(\hat{\mu}_{MC}) - \text{Var}(\hat{\mu}_{SS}) = \frac{1}{N}\sum_k p_k(\mu_k - \mu)^2 \geq 0
$$

**Conclusion:** $\text{Var}(\hat{\mu}_{SS}) \leq \text{Var}(\hat{\mu}_{MC})$ always.
Equality holds only when all stratum means are identical ($\mu_k = \mu$ for all $k$).
$\blacksquare$

**Interpretation.** Stratification removes the between-strata variance,
keeping only the within-strata variance. The more heterogeneous the strata
means, the greater the variance reduction.

### Application to the Budget Model

Stratify on the salary level of the first employee (as a proxy for overall
salary distribution):

- **Low:** $S_1 < Q_{0.33}$ (bottom third)
- **Medium:** $Q_{0.33} \leq S_1 < Q_{0.67}$ (middle third)
- **High:** $S_1 \geq Q_{0.67}$ (top third)

Each stratum has $p_k = 1/3$ with proportional allocation.
