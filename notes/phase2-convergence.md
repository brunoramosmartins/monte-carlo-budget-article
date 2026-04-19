# Phase 2 — Convergence Theorems

## Overview

This phase establishes the theoretical backbone of Monte Carlo simulation:
the **Law of Large Numbers**. The proof chain is:

$$
\text{Markov's inequality} \;\longrightarrow\; \text{Chebyshev's inequality} \;\longrightarrow\; \text{Weak Law of Large Numbers}
$$

Each link in this chain is derived from scratch. The Strong Law of Large
Numbers is stated with intuition and a proof sketch.

---

## 1. Markov's Inequality

### Statement

**Theorem 1.1 (Markov's Inequality).** Let $X$ be a non-negative random
variable with finite expectation. Then for any $a > 0$:

$$
P(X \geq a) \leq \frac{E[X]}{a}
$$

### Proof

Since $X \geq 0$, we can write:

$$
E[X] = \int_0^{\infty} x \, f_X(x) \, dx
$$

Split the integral at $a$:

$$
E[X] = \int_0^{a} x \, f_X(x) \, dx + \int_a^{\infty} x \, f_X(x) \, dx
$$

The first integral is non-negative (since $x \geq 0$ and $f_X(x) \geq 0$), so:

$$
E[X] \geq \int_a^{\infty} x \, f_X(x) \, dx
$$

In the region $x \geq a$, we have $x \geq a$, so:

$$
\int_a^{\infty} x \, f_X(x) \, dx \geq \int_a^{\infty} a \, f_X(x) \, dx = a \int_a^{\infty} f_X(x) \, dx = a \, P(X \geq a)
$$

Combining:

$$
E[X] \geq a \, P(X \geq a)
$$

$$
P(X \geq a) \leq \frac{E[X]}{a} \qquad \blacksquare
$$

### Numerical Example

Let $S \sim \text{LogNormal}(9.2, 0.09)$ represent a monthly salary with
$E[S] \approx 10{,}362$.

**Question:** What is the upper bound on the probability that a salary exceeds
R\$ 30,000?

By Markov:

$$
P(S \geq 30{,}000) \leq \frac{E[S]}{30{,}000} = \frac{10{,}362}{30{,}000} \approx 0.345
$$

The true probability (computed from the LogNormal CDF) is approximately 0.018.
Markov gives a loose but universally valid bound — it uses only the mean,
no information about the distribution's shape.

### Remark on Generality

Markov's inequality is powerful precisely because it is weak: it requires
only $E[X] < \infty$ and $X \geq 0$. No distributional assumptions are needed.
This generality is what makes it the foundation for Chebyshev and the LLN.

---

## 2. Chebyshev's Inequality

### Statement

**Theorem 2.1 (Chebyshev's Inequality).** Let $X$ be a random variable with
finite mean $\mu = E[X]$ and finite variance $\sigma^2 = \text{Var}(X)$. Then
for any $\epsilon > 0$:

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2}
$$

Equivalently, setting $\epsilon = k\sigma$ for $k > 0$:

$$
P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}
$$

### Proof (as a Corollary of Markov)

Define $Y = (X - \mu)^2$. Note that:

- $Y \geq 0$ (it is a squared quantity)
- $E[Y] = E[(X - \mu)^2] = \sigma^2$

The event $\{|X - \mu| \geq \epsilon\}$ is equivalent to
$\{(X - \mu)^2 \geq \epsilon^2\}$, which is $\{Y \geq \epsilon^2\}$.

Apply Markov's inequality to $Y$ with threshold $a = \epsilon^2$:

$$
P(Y \geq \epsilon^2) \leq \frac{E[Y]}{\epsilon^2}
$$

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2} \qquad \blacksquare
$$

### Numerical Example

Consider the total budget cost with $E[X_{\text{total}}] \approx 11{,}554{,}495$
and $\text{SD}(X_{\text{total}}) \approx 492{,}747$ (from Phase 1).

**Question:** What is the upper bound on the probability that the budget
deviates from its expected value by more than R\$ 1,000,000?

$$
P(|X_{\text{total}} - 11{,}554{,}495| \geq 1{,}000{,}000) \leq \frac{(492{,}747)^2}{(1{,}000{,}000)^2} = \frac{2.428 \times 10^{11}}{10^{12}} \approx 0.243
$$

With $k\sigma$ form: $\epsilon = 1{,}000{,}000 \approx 2.03\sigma$, so
$P \leq 1/(2.03)^2 \approx 0.243$.

**Interpretation:** Chebyshev guarantees that at most 24.3% of budget outcomes
deviate from the mean by more than R\$ 1M. The bound uses only the mean and
variance — no distributional assumptions.

### Comparison of Bounds

| Bound | Information Used | Tightness |
|-------|-----------------|-----------|
| Markov | Mean only | Very loose |
| Chebyshev | Mean + variance | Moderate |
| CLT (Phase 3) | Mean + variance + normality | Tight |

---

## 3. Weak Law of Large Numbers

### Setup

Let $X_1, X_2, \ldots, X_n$ be **independent and identically distributed (i.i.d.)**
random variables with:

- $E[X_i] = \mu$ (finite)
- $\text{Var}(X_i) = \sigma^2$ (finite)

Define the **sample mean**:

$$
\bar{X}_n = \frac{1}{n} \sum_{i=1}^n X_i
$$

### Statement

**Theorem 3.1 (Weak Law of Large Numbers).** Under the conditions above:

$$
\bar{X}_n \xrightarrow{P} \mu \quad \text{as } n \to \infty
$$

That is, for every $\epsilon > 0$:

$$
\lim_{n \to \infty} P(|\bar{X}_n - \mu| \geq \epsilon) = 0
$$

### Proof (via Chebyshev)

**Step 1: Compute $E[\bar{X}_n]$.**

By linearity of expectation:

$$
E[\bar{X}_n] = E\left[\frac{1}{n}\sum_{i=1}^n X_i\right] = \frac{1}{n}\sum_{i=1}^n E[X_i] = \frac{1}{n} \cdot n\mu = \mu
$$

So $\bar{X}_n$ is an **unbiased estimator** of $\mu$.

**Step 2: Compute $\text{Var}(\bar{X}_n)$.**

Since $X_i$ are independent:

$$
\text{Var}(\bar{X}_n) = \text{Var}\left(\frac{1}{n}\sum_{i=1}^n X_i\right) = \frac{1}{n^2}\sum_{i=1}^n \text{Var}(X_i) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}
$$

**Step 3: Apply Chebyshev's inequality to $\bar{X}_n$.**

For any $\epsilon > 0$:

$$
P(|\bar{X}_n - \mu| \geq \epsilon) \leq \frac{\text{Var}(\bar{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2}
$$

**Step 4: Take the limit.**

$$
\lim_{n \to \infty} P(|\bar{X}_n - \mu| \geq \epsilon) \leq \lim_{n \to \infty} \frac{\sigma^2}{n\epsilon^2} = 0
$$

Since probabilities are non-negative:

$$
\lim_{n \to \infty} P(|\bar{X}_n - \mu| \geq \epsilon) = 0 \qquad \blacksquare
$$

### Numerical Example

For monthly salaries $S_i \sim \text{LogNormal}(9.2, 0.09)$ with
$E[S_i] \approx 10{,}362$ and $\text{Var}(S_i) \approx 10{,}117{,}947$:

**Question:** If we average $N = 1{,}000$ salary draws, what is the Chebyshev
bound on the probability that $\bar{S}_N$ differs from $E[S]$ by more than
R\$ 500?

$$
P(|\bar{S}_N - 10{,}362| \geq 500) \leq \frac{10{,}117{,}947}{1{,}000 \times 500^2} = \frac{10{,}117{,}947}{250{,}000{,}000} \approx 0.0405
$$

With 1,000 samples, Chebyshev guarantees at most a 4.05% chance that the
sample mean deviates from the true mean by more than R\$ 500.

### Interpretation for Monte Carlo

The WLLN says: **the sample mean of $N$ simulated budgets converges to
$E[X_{\text{total}}]$ as $N \to \infty$.**

More concretely:

1. Each simulation produces one sample $X_i$ from the budget cost distribution.
2. The average of $N$ simulations, $\bar{X}_N$, is our Monte Carlo estimate.
3. The WLLN guarantees that this estimate converges to the true expected cost.
4. The rate of convergence is controlled by $\sigma^2 / (N\epsilon^2)$ — more
   samples or larger tolerance both make the bound smaller.

This is the fundamental theorem that justifies Monte Carlo estimation.
Without it, averaging random simulations would be nothing more than numerology.

---

## 4. Strong Law of Large Numbers

### Statement

**Theorem 4.1 (Strong Law of Large Numbers — Kolmogorov).** Let $X_1, X_2, \ldots$
be i.i.d. random variables with $E[|X_i|] < \infty$ and $E[X_i] = \mu$. Then:

$$
P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1
$$

That is, $\bar{X}_n \xrightarrow{a.s.} \mu$ (almost sure convergence).

### Convergence Modes: In Probability vs Almost Sure

The key difference between the Weak and Strong LLN is the **mode of convergence**:

| Mode | Notation | Meaning |
|------|----------|---------|
| In probability | $\bar{X}_n \xrightarrow{P} \mu$ | For every fixed $\epsilon > 0$, $P(\|\bar{X}_n - \mu\| \geq \epsilon) \to 0$ |
| Almost sure | $\bar{X}_n \xrightarrow{a.s.} \mu$ | The set of $\omega$ where $\bar{X}_n(\omega) \not\to \mu$ has probability zero |

**Analogy.** Convergence in probability says: "for any snapshot in time, the
sample mean is probably close to $\mu$." Almost sure convergence says:
"the entire trajectory of $\bar{X}_n$ eventually settles at $\mu$, with no
exceptions except on a set of probability zero."

Almost sure convergence is strictly stronger:

$$
\bar{X}_n \xrightarrow{a.s.} \mu \implies \bar{X}_n \xrightarrow{P} \mu
$$

The converse is false in general.

### Intuition for the Proof

The full proof of the SLLN (e.g., Kolmogorov's proof) relies on tools from
measure theory, particularly:

1. **Borel-Cantelli Lemma:** If $\sum_n P(A_n) < \infty$, then
   $P(\limsup_n A_n) = 0$ — that is, only finitely many of the events $A_n$
   occur, almost surely.

2. **Fourth moment bound:** For i.i.d. variables with finite fourth moment
   ($E[X^4] < \infty$), one can show $\sum_n P(|\bar{X}_n - \mu| \geq \epsilon) < \infty$
   by bounding $E[(\bar{X}_n - \mu)^4]$ and applying Markov's inequality.

3. **Kronecker's lemma + truncation:** For the general case (only
   $E[|X|] < \infty$ required), the proof uses truncation arguments and
   Kronecker's lemma to handle variables without finite variance.

**Why we state but don't fully prove:** The SLLN requires measure-theoretic
machinery (Borel-Cantelli, almost sure convergence) that is beyond the scope
of this article. The WLLN proof via Chebyshev is elementary and sufficient
to justify Monte Carlo — the SLLN is the stronger guarantee that "the
simulation will eventually get the right answer, period."

### Proof Sketch (Fourth Moment Version)

Assume $E[X^4] < \infty$ in addition to i.i.d. with mean $\mu$ and
variance $\sigma^2$.

**Step 1.** Compute $E[(\bar{X}_n - \mu)^4]$.

Let $Y_i = X_i - \mu$, so $E[Y_i] = 0$. Then:

$$
E\left[\left(\frac{1}{n}\sum Y_i\right)^4\right] = \frac{1}{n^4} E\left[\left(\sum Y_i\right)^4\right]
$$

Expanding $(\sum Y_i)^4$ and using independence ($E[Y_i Y_j Y_k Y_l] = 0$
unless indices are paired), the dominant terms give:

$$
E[(\bar{X}_n - \mu)^4] = O\left(\frac{1}{n^2}\right)
$$

**Step 2.** Apply Markov's inequality with $Y = (\bar{X}_n - \mu)^4$:

$$
P(|\bar{X}_n - \mu| \geq \epsilon) = P((\bar{X}_n - \mu)^4 \geq \epsilon^4) \leq \frac{E[(\bar{X}_n - \mu)^4]}{\epsilon^4} = O\left(\frac{1}{n^2}\right)
$$

**Step 3.** Since $\sum_{n=1}^{\infty} 1/n^2 = \pi^2/6 < \infty$, by
Borel-Cantelli:

$$
P(\limsup_n \{|\bar{X}_n - \mu| \geq \epsilon\}) = 0
$$

This means: almost surely, only finitely many of the events
$\{|\bar{X}_n - \mu| \geq \epsilon\}$ occur. Since this holds for every
$\epsilon > 0$, we get $\bar{X}_n \to \mu$ almost surely. $\blacksquare$

### Relevance to Monte Carlo

For our budget simulation:

- **WLLN guarantees:** "With enough simulations, the Monte Carlo estimate
  $\bar{X}_N$ is probably close to $E[X_{\text{total}}]$."

- **SLLN guarantees:** "The Monte Carlo estimate $\bar{X}_N$ **will** converge
  to $E[X_{\text{total}}]$ — not just probably, but with certainty (up to a
  measure-zero set)."

In practice, the SLLN assures us that Monte Carlo is not a gamble: given enough
computational budget, the answer is correct. The remaining question — "how
close is the estimate for a given $N$?" — is answered by the Central Limit
Theorem (Phase 3).

---

## 5. Chebyshev Bounds for Monte Carlo

### Deriving the Bound

From the WLLN proof, we established:

$$
P(|\bar{X}_N - \mu| \geq \epsilon) \leq \frac{\sigma^2}{N \epsilon^2}
$$

We can invert this to find the **minimum $N$** for a desired guarantee.
Given a tolerance $\epsilon$ and a confidence level $1 - \alpha$ (i.e., we want
$P(|\bar{X}_N - \mu| \geq \epsilon) \leq \alpha$):

$$
\frac{\sigma^2}{N \epsilon^2} \leq \alpha \implies N \geq \frac{\sigma^2}{\alpha \epsilon^2}
$$

### Example: Budget Simulation

For the total budget with $\sigma \approx 492{,}747$:

**Question:** How many simulations are needed so that the Chebyshev bound
guarantees $P(|\bar{X}_N - E[X]| \geq 100{,}000) \leq 0.05$?

$$
N \geq \frac{(492{,}747)^2}{0.05 \times (100{,}000)^2} = \frac{2.428 \times 10^{11}}{5 \times 10^{8}} \approx 486
$$

According to Chebyshev, we need at least 486 simulations. The CLT (Phase 3)
will give a much tighter answer.

### Chebyshev Confidence Band

For a running simulation with $n$ samples so far, the Chebyshev bound defines
a confidence band around $\mu$:

$$
\mu \in \left[\bar{X}_n - \frac{\sigma}{\sqrt{n\alpha}}, \; \bar{X}_n + \frac{\sigma}{\sqrt{n\alpha}}\right]
$$

with probability at least $1 - \alpha$.

This band shrinks as $O(1/\sqrt{n})$, visually demonstrating convergence.
The convergence notebook overlays this band on the running mean plot.
