# Exercises — Phase 1: Probability Foundations

These exercises are designed to be solved on paper. They reinforce the
derivations from `notes/phase1-probability.md` and build intuition for the
budget model.

---

## Proofs (paper)

### Exercise 1 — LogNormal Expected Value

**Prove** that for $X \sim \text{LogNormal}(\mu, \sigma^2)$:

$$
E[X] = e^{\mu + \sigma^2/2}
$$

*Hint: write $X = e^Y$ where $Y \sim N(\mu, \sigma^2)$, so $E[X] = E[e^Y] = M_Y(1)$.
Use the MGF of the Normal distribution derived in Section 5.1 of the notes.*

---

### Exercise 2 — Variance of a Sum (General Case)

**Prove** that:

$$
\text{Var}(X_1 + X_2 + \cdots + X_n) = \sum_{i=1}^n \text{Var}(X_i) + 2\sum_{i<j} \text{Cov}(X_i, X_j)
$$

*Start from the definition $\text{Var}(S) = E[(S - E[S])^2]$ where
$S = \sum X_i$. Expand the square and apply linearity of expectation. Count
the cross terms carefully.*

---

### Exercise 3 — Variance of the Sample Mean

**Prove** that if $X_1, \ldots, X_n$ are i.i.d. with mean $\mu$ and variance
$\sigma^2$, then:

$$
\text{Var}(\bar{X}_n) = \frac{\sigma^2}{n}
$$

where $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$.

*This result is the engine behind Monte Carlo convergence: averaging $n$
independent simulations reduces variance by a factor of $n$. Use
Theorem 3.2 (variance of a linear transformation) and the i.i.d. assumption.*

---

### Exercise 4 — Jensen's Inequality (Convex Case)

**Prove** Jensen's inequality for the convex function $g(x) = x^2$:

$$
E[X^2] \geq (E[X])^2
$$

*Consequence: variance is always non-negative, since
$\text{Var}(X) = E[X^2] - (E[X])^2 \geq 0$.*

*Approach: consider the random variable $(X - \mu)^2 \geq 0$ and take
expectations. Alternatively, use the fact that for any convex function $g$
and any random variable $X$: $g(E[X]) \leq E[g(X)]$.*

---

## Computations (paper)

### Exercise 5 — Salary Distribution Moments

Let $S \sim \text{LogNormal}(9.2, 0.3^2)$ (i.e., $\mu = 9.2$, $\sigma^2 = 0.09$).

**Compute by hand:**

1. $E[S]$
2. $\text{Var}(S)$
3. $\text{SD}(S)$

**Interpret:** What does a monthly salary with these parameters look like? What
is the median salary? (Recall: the median of $\text{LogNormal}(\mu, \sigma^2)$
is $e^{\mu}$.) How does the mean compare to the median, and what does this say
about the skewness?

---

### Exercise 6 — Annual Salary Cost (Analytical)

An IT team has $n = 50$ employees with i.i.d. salaries
$S_i \sim \text{LogNormal}(9.2, 0.3^2)$ and benefits multiplier $\beta = 1.80$.

The annual salary cost is:

$$
T_1 = \sum_{i=1}^{50} S_i \cdot \beta \cdot 12
$$

**Compute analytically:**

1. $E[T_1]$ — keep symbolic first, then plug in numbers
2. $\text{Var}(T_1)$ — use the i.i.d. assumption and Theorem 3.2
3. $\text{SD}(T_1)$

**Check:** Does your $E[T_1]$ match the value in `docs/model-design.md`?

---

### Exercise 7 — Incident Cost (Law of Total Expectation)

Severe incidents follow $I \sim \text{Poisson}(3)$ and each incident costs
$C \sim \text{LogNormal}(10.5, 0.5^2)$. The incidents and costs are independent.

The total incident cost is:

$$
T_3 = \sum_{j=1}^{I} C_j
$$

1. Using the **law of total expectation**, compute
   $E[T_3] = E[I] \cdot E[C]$. Under what assumption is this valid?

2. Using the **law of total variance**, compute $\text{Var}(T_3)$.
   *Hint: $\text{Var}(T_3) = E[I] \cdot \text{Var}(C) + \text{Var}(I) \cdot (E[C])^2 = \lambda \cdot E[C^2]$.*

3. Compute $\text{SD}(T_3)$. Is the incident cost component more or less
   variable (relative to its mean) than the salary component?
