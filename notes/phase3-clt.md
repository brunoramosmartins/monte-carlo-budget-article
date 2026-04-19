# Phase 3 — Central Limit Theorem and Confidence Intervals

## Overview

The LLN (Phase 2) tells us **that** the Monte Carlo estimator converges.
The Central Limit Theorem tells us **how fast** — and gives us the tool to
build confidence intervals. This phase proves the CLT via the MGF approach,
states the Berry-Esseen rate, and derives the CI formulas that make Monte
Carlo practically useful.

---

## 1. Moment Generating Functions — Review

### Definition

The **moment generating function (MGF)** of a random variable $X$ is:

$$
M_X(t) = E[e^{tX}]
$$

defined for all $t$ in a neighbourhood of zero where the expectation exists.

### Key Properties (from Phase 1)

1. **Moment extraction:** $E[X^n] = M_X^{(n)}(0)$.
2. **Uniqueness:** If $M_X(t) = M_Y(t)$ for all $t$ in a neighbourhood of
   zero, then $X \stackrel{d}{=} Y$.
3. **Sum of independents:** If $X \perp Y$, then $M_{X+Y}(t) = M_X(t) \cdot M_Y(t)$.

### MGF of the Standard Normal

For $Z \sim N(0, 1)$ (derived in Phase 1, Section 5.1):

$$
M_Z(t) = e^{t^2/2}
$$

This is the "target" MGF: if we can show that the standardised sample mean
has an MGF converging to $e^{t^2/2}$, then by uniqueness the standardised
sample mean converges in distribution to $N(0, 1)$.

---

## 2. Central Limit Theorem

### Statement

**Theorem 2.1 (Central Limit Theorem).** Let $X_1, X_2, \ldots$ be i.i.d.
random variables with $E[X_i] = \mu$, $\text{Var}(X_i) = \sigma^2 \in (0, \infty)$,
and $M_{X_i}(t)$ existing in a neighbourhood of zero. Define:

$$
Z_n = \frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} = \frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma}
$$

Then:

$$
Z_n \xrightarrow{d} N(0, 1) \quad \text{as } n \to \infty
$$

That is, for every $x \in \mathbb{R}$:

$$
\lim_{n \to \infty} P(Z_n \leq x) = \Phi(x) = \int_{-\infty}^x \frac{1}{\sqrt{2\pi}} e^{-u^2/2} \, du
$$

### Proof (MGF Approach)

**Strategy:** Show that $M_{Z_n}(t) \to e^{t^2/2}$ for all $t$ near zero.
By the continuity theorem for MGFs, this implies $Z_n \xrightarrow{d} N(0, 1)$.

**Step 1: Standardise.**

Define $W_i = \frac{X_i - \mu}{\sigma}$, so that $E[W_i] = 0$ and
$\text{Var}(W_i) = 1$. Then:

$$
Z_n = \frac{1}{\sqrt{n}} \sum_{i=1}^n W_i
$$

**Step 2: Compute the MGF of $Z_n$.**

Since $W_1, \ldots, W_n$ are i.i.d.:

$$
M_{Z_n}(t) = E\left[\exp\left(t \cdot \frac{1}{\sqrt{n}} \sum_{i=1}^n W_i\right)\right] = E\left[\prod_{i=1}^n \exp\left(\frac{t}{\sqrt{n}} W_i\right)\right]
$$

By independence:

$$
= \prod_{i=1}^n E\left[\exp\left(\frac{t}{\sqrt{n}} W_i\right)\right] = \left[M_W\left(\frac{t}{\sqrt{n}}\right)\right]^n
$$

**Step 3: Taylor expand $\log M_W(s)$ around $s = 0$.**

Let $s = t / \sqrt{n}$. We expand $\log M_W(s)$ using the known properties
of $W$ (mean 0, variance 1).

First, expand $M_W(s)$ itself. By definition:

$$
M_W(s) = E[e^{sW}] = E\left[1 + sW + \frac{s^2 W^2}{2} + \frac{s^3 W^3}{6} + \cdots\right]
$$

$$
= 1 + s \, E[W] + \frac{s^2}{2} E[W^2] + \frac{s^3}{6} E[W^3] + \cdots
$$

Since $E[W] = 0$ and $E[W^2] = \text{Var}(W) = 1$:

$$
M_W(s) = 1 + \frac{s^2}{2} + \frac{s^3}{6} E[W^3] + O(s^4)
$$

Now take the logarithm. Using $\log(1 + u) = u - u^2/2 + O(u^3)$ with
$u = s^2/2 + O(s^3)$:

$$
\log M_W(s) = \frac{s^2}{2} + O(s^3)
$$

The $O(s^3)$ term absorbs the third moment and higher terms. (This is where
we use the assumption that the MGF exists in a neighbourhood of zero, which
ensures the Taylor series is valid.)

**Step 4: Substitute $s = t/\sqrt{n}$.**

$$
\log M_W\left(\frac{t}{\sqrt{n}}\right) = \frac{1}{2}\left(\frac{t}{\sqrt{n}}\right)^2 + O\left(\left(\frac{t}{\sqrt{n}}\right)^3\right)
$$

$$
= \frac{t^2}{2n} + O\left(\frac{t^3}{n^{3/2}}\right)
$$

**Step 5: Compute $\log M_{Z_n}(t)$.**

$$
\log M_{Z_n}(t) = n \cdot \log M_W\left(\frac{t}{\sqrt{n}}\right) = n \left[\frac{t^2}{2n} + O\left(\frac{t^3}{n^{3/2}}\right)\right]
$$

$$
= \frac{t^2}{2} + O\left(\frac{t^3}{\sqrt{n}}\right)
$$

**Step 6: Take the limit.**

$$
\lim_{n \to \infty} \log M_{Z_n}(t) = \frac{t^2}{2}
$$

Therefore:

$$
\lim_{n \to \infty} M_{Z_n}(t) = e^{t^2/2}
$$

This is the MGF of $N(0, 1)$.

**Step 7: Conclude by uniqueness.**

By the continuity theorem for moment generating functions: if $M_{Z_n}(t) \to M_Z(t)$
for all $t$ in a neighbourhood of zero and $M_Z$ is the MGF of some
distribution, then $Z_n \xrightarrow{d} Z$.

Since $e^{t^2/2}$ is the MGF of $N(0, 1)$:

$$
Z_n = \frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \xrightarrow{d} N(0, 1) \qquad \blacksquare
$$

### What Each Step Achieves

| Step | Action | Why It Works |
|------|--------|-------------|
| 1 | Standardise to $W_i$ | Ensures $E[W] = 0$, $\text{Var}(W) = 1$ — simplifies Taylor |
| 2 | Factor MGF via independence | Reduces to a single MGF raised to power $n$ |
| 3 | Taylor expand $\log M_W(s)$ | Key insight: $\log M_W(s) = s^2/2 + O(s^3)$ because mean=0, var=1 |
| 4 | Substitute $s = t/\sqrt{n}$ | The $\sqrt{n}$ normalisation makes the $O(s^3)$ term vanish |
| 5 | Multiply by $n$ | The $t^2/(2n)$ term becomes $t^2/2$; the remainder vanishes |
| 6 | Take limit | Remainder $O(t^3/\sqrt{n}) \to 0$ |
| 7 | Uniqueness theorem | MGF convergence implies convergence in distribution |

---

## 3. Berry-Esseen Theorem

### Statement

**Theorem 3.1 (Berry-Esseen).** Let $X_1, \ldots, X_n$ be i.i.d. with
$E[X_i] = 0$, $E[X_i^2] = \sigma^2 > 0$, and $E[|X_i|^3] = \rho < \infty$.
Then:

$$
\sup_{x \in \mathbb{R}} \left|P\left(\frac{\bar{X}_n}{\sigma/\sqrt{n}} \leq x\right) - \Phi(x)\right| \leq \frac{C \rho}{\sigma^3 \sqrt{n}}
$$

where $C$ is a universal constant. The best known bound is $C \leq 0.4748$.

### Interpretation

- The CLT says the Normal approximation gets better as $n \to \infty$.
  Berry-Esseen quantifies **how fast**: the error decays as $O(1/\sqrt{n})$.

- For $n = 30$: the maximum approximation error is at most $\approx C\rho / (\sigma^3 \sqrt{30})$.

- For $n = 100$: the error is roughly $\sqrt{30/100} \approx 0.55$ times the
  error at $n = 30$ — almost halved.

### Practical Rule of Thumb

The CLT approximation is often considered "good enough" when $n \geq 30$.
Berry-Esseen makes this precise: for symmetric distributions with moderate
third moments, the approximation error at $n = 30$ is typically a few
percentage points.

### Numerical Example

For standardised salary costs with $E[|W|^3] = \rho/\sigma^3 = 2.5$:

- At $n = 30$: bound $\leq 0.4748 \times 2.5 / \sqrt{30} \approx 0.217$
- At $n = 100$: bound $\leq 0.4748 \times 2.5 / \sqrt{100} \approx 0.119$

These are worst-case bounds over all $x$. In practice, the approximation is
much better in the "bulk" of the distribution and worse only in the tails.

---

## 4. Confidence Intervals for Monte Carlo

### From CLT to Confidence Intervals

The CLT gives us:

$$
\frac{\bar{X}_N - \mu}{\sigma / \sqrt{N}} \;\dot{\sim}\; N(0, 1) \quad \text{for large } N
$$

Therefore, for the standard Normal quantile $z_{\alpha/2}$ (e.g., $z_{0.025} = 1.96$
for 95% confidence):

$$
P\left(-z_{\alpha/2} \leq \frac{\bar{X}_N - \mu}{\sigma / \sqrt{N}} \leq z_{\alpha/2}\right) \approx 1 - \alpha
$$

Rearranging for $\mu$:

$$
P\left(\bar{X}_N - z_{\alpha/2} \frac{\sigma}{\sqrt{N}} \leq \mu \leq \bar{X}_N + z_{\alpha/2} \frac{\sigma}{\sqrt{N}}\right) \approx 1 - \alpha
$$

### Practical Form (with sample standard deviation)

In practice, $\sigma$ is unknown. We replace it with the sample standard
deviation $s_N$:

$$
\text{CI}_{1-\alpha} = \left[\bar{X}_N - z_{\alpha/2} \frac{s_N}{\sqrt{N}}, \;\; \bar{X}_N + z_{\alpha/2} \frac{s_N}{\sqrt{N}}\right]
$$

This is valid for large $N$ because:
1. By the WLLN, $s_N \xrightarrow{P} \sigma$ (consistency of the sample variance).
2. By Slutsky's theorem, replacing $\sigma$ with $s_N$ preserves the limiting
   distribution.

### Standard Error and Half-Width

The **Monte Carlo standard error** is:

$$
\text{SE} = \frac{s_N}{\sqrt{N}}
$$

The **confidence interval half-width** (precision) is:

$$
\epsilon = z_{\alpha/2} \cdot \text{SE} = z_{\alpha/2} \cdot \frac{s_N}{\sqrt{N}}
$$

### Common Quantiles

| Confidence Level | $\alpha$ | $z_{\alpha/2}$ |
|-----------------|----------|----------------|
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.960 |
| 99% | 0.01 | 2.576 |

---

## 5. Choosing $N$: How Many Simulations?

### Derivation

Given a desired half-width $\epsilon$ and confidence level $1 - \alpha$, we
need:

$$
z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{N}} \leq \epsilon
$$

Solving for $N$:

$$
\frac{\sigma}{\sqrt{N}} \leq \frac{\epsilon}{z_{\alpha/2}}
$$

$$
\sqrt{N} \geq \frac{z_{\alpha/2} \cdot \sigma}{\epsilon}
$$

$$
N \geq \left(\frac{z_{\alpha/2} \cdot \sigma}{\epsilon}\right)^2
$$

### Practical Procedure (Two-Stage)

Since $\sigma$ is unknown before running the simulation:

1. **Pilot run:** Run $N_0$ simulations (e.g., $N_0 = 100$) and compute $s_{N_0}$.
2. **Compute required $N$:** $N \geq (z_{\alpha/2} \cdot s_{N_0} / \epsilon)^2$.
3. **Run remaining simulations:** Generate $N - N_0$ additional samples.
4. **Recompute CI** using all $N$ samples.

### Example: Budget Simulation

**Setup:** From the pilot run, $s \approx 492{,}747$ (budget standard deviation).
We want 95% confidence with $\epsilon = R\$ \, 100{,}000$.

$$
N \geq \left(\frac{1.96 \times 492{,}747}{100{,}000}\right)^2 = \left(\frac{965{,}784}{100{,}000}\right)^2 = (9.658)^2 \approx 94
$$

**Only 94 simulations** are needed for the CLT-based CI to guarantee
±R\$ 100K precision at 95% confidence.

Compare with the Chebyshev bound from Phase 2, which required $N \geq 486$.
The CLT gives a **5× improvement** because it exploits the Normal
approximation instead of using only mean and variance.

### Scaling Law

From the formula $N \propto 1/\epsilon^2$:

- Halving the precision ($\epsilon/2$) requires **4× more simulations**.
- To go from ±R\$ 100K to ±R\$ 50K: $N$ increases from 94 to $94 \times 4 = 376$.
- To go from ±R\$ 100K to ±R\$ 10K: $N$ increases from 94 to $94 \times 100 = 9{,}400$.

### Comparison: Chebyshev vs CLT

| Method | Required $N$ for ±R\$ 100K at 95% | Information Used |
|--------|----------------------------------|-----------------|
| Chebyshev | 486 | Mean + variance only |
| CLT | 94 | Mean + variance + Normal approximation |
| Ratio | 5.2× | CLT is 5× more efficient |

---

## 6. Connection to Monte Carlo

### The Complete Picture (Phases 1–3)

| Phase | Theorem | What It Tells Us |
|-------|---------|-----------------|
| Phase 1 | Linearity of $E$, properties of $\text{Var}$ | How to compute analytical moments of the budget |
| Phase 2 | Law of Large Numbers | The MC estimate $\bar{X}_N$ **converges** to $E[X]$ |
| Phase 3 | Central Limit Theorem | The MC estimate has a **quantifiable error** of $O(1/\sqrt{N})$ |

Together, these three phases provide the full mathematical justification for
Monte Carlo simulation:

1. **The estimator is well-defined** (Phase 1: the budget cost has finite moments).
2. **The estimator converges** (Phase 2: LLN guarantees $\bar{X}_N \to \mu$).
3. **We can bound the error** (Phase 3: CLT gives $\bar{X}_N \approx \mu \pm z \cdot \sigma/\sqrt{N}$).

Phase 4 will formalise the Monte Carlo estimator itself and implement it.
