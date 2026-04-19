# Exercises — Phase 2: Convergence Theorems

These exercises reinforce the proof chain Markov → Chebyshev → WLLN and
build intuition for Monte Carlo convergence. Solve on paper.

---

## Proofs (paper)

### Exercise 1 — Prove Markov's Inequality

**Prove** Markov's inequality from the definition of expectation: for a
non-negative random variable $X$ and $a > 0$:

$$
P(X \geq a) \leq \frac{E[X]}{a}
$$

*Hint: split the integral $E[X] = \int_0^{\infty} x \, f_X(x) \, dx$ at $a$
and bound the integrand in the region $[a, \infty)$.*

---

### Exercise 2 — Derive Chebyshev's Inequality

**Derive** Chebyshev's inequality as a corollary of Markov's inequality applied
to $Y = (X - \mu)^2$:

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2}
$$

*Show each step of the substitution: define $Y$, verify $Y \geq 0$,
identify the equivalent event, apply Markov, and simplify.*

---

### Exercise 3 — Prove the Weak Law of Large Numbers

**Prove** the Weak Law of Large Numbers for i.i.d. random variables with
finite variance:

If $X_1, \ldots, X_n$ are i.i.d. with $E[X_i] = \mu$ and
$\text{Var}(X_i) = \sigma^2 < \infty$, then for every $\epsilon > 0$:

$$
\lim_{n \to \infty} P(|\bar{X}_n - \mu| \geq \epsilon) = 0
$$

*Use Chebyshev's inequality on $\bar{X}_n$. The proof has four steps:
(1) compute $E[\bar{X}_n]$, (2) compute $\text{Var}(\bar{X}_n)$,
(3) apply Chebyshev, (4) take the limit.*

---

### Exercise 4 — Variance Decay: Necessary but Not Sufficient?

**Prove** that $\text{Var}(\bar{X}_n) \to 0$ is **necessary but not sufficient**
for convergence in probability.

*Part (a): Show that convergence in probability implies
$\text{Var}(\bar{X}_n) \to 0$ when the variance exists. (Hint: if
$\bar{X}_n \xrightarrow{P} \mu$, then $E[(\bar{X}_n - \mu)^2] \to 0$
under bounded convergence.)*

*Part (b): Explain why Chebyshev "closes the gap" — that is, why
$\text{Var}(\bar{X}_n) \to 0$ is actually sufficient when combined with the
Chebyshev inequality. What role does the bound
$P(|\bar{X}_n - \mu| \geq \epsilon) \leq \text{Var}(\bar{X}_n)/\epsilon^2$
play?*

---

## Computations (paper)

### Exercise 5 — Minimum N via Chebyshev

For $X \sim \text{LogNormal}(9.2, 0.09)$ (monthly salary):

1. Compute $E[X]$ and $\text{Var}(X)$.
2. Using Chebyshev's inequality, find the minimum $N$ such that:

$$
P(|\bar{X}_N - E[X]| \geq 500) \leq 0.05
$$

3. Interpret: what does this $N$ mean in the context of Monte Carlo simulation
   of salary averages?

---

### Exercise 6 — Chebyshev Bound on a Simulation

You simulate a budget 1,000 times and get $\bar{X}_{1000} = 12{,}340{,}000$
with sample variance $s^2 = 2.5 \times 10^{12}$.

1. Using Chebyshev, give an upper bound on:

$$
P(|E[X] - 12{,}340{,}000| \geq 100{,}000)
$$

2. Is this bound tight? What additional information would give a tighter bound?

3. How many simulations would be needed to reduce this Chebyshev bound to 0.01?
