# Phase 1 — Probability Foundations

## 1. Random Variables

### Definition

A **random variable** is a measurable function from a sample space to the real
numbers:

$$
X : \Omega \to \mathbb{R}
$$

where $(\Omega, \mathcal{F}, P)$ is a probability space:

- $\Omega$ is the set of all possible outcomes (the sample space),
- $\mathcal{F}$ is a $\sigma$-algebra of events (subsets of $\Omega$),
- $P$ is a probability measure on $\mathcal{F}$.

The measurability condition ensures that for any Borel set $B \subseteq \mathbb{R}$,
the preimage $X^{-1}(B) = \{\omega \in \Omega : X(\omega) \in B\}$ is in $\mathcal{F}$,
so that $P(X \in B)$ is well-defined.

### Connection to the Budget Model

In our budget model (here instantiated for IT headcount), each salary $S_i$ is a random variable:

$$
S_i : \Omega \to \mathbb{R}^+
$$

Here $\Omega$ represents the set of all "possible worlds" — all ways the next
fiscal year could unfold. A specific $\omega \in \Omega$ fixes every employee's
salary, overtime hours, and incident count. The value $S_i(\omega)$ is the
salary of employee $i$ in that particular scenario.

When we say "$S_i \sim \text{LogNormal}(9.2, 0.3^2)$", we are specifying the
**distribution** of $S_i$ — that is, the probability measure
$P_{S_i}(B) = P(S_i \in B)$ for every Borel set $B$.

### Discrete vs Continuous

A random variable $X$ is **discrete** if it takes values in a countable set
$\{x_1, x_2, \ldots\}$. Its distribution is characterised by the **probability
mass function (PMF)**:

$$
p_X(x) = P(X = x), \quad \sum_{x} p_X(x) = 1
$$

A random variable $X$ is **continuous** if there exists a non-negative function
$f_X$ such that for every interval $[a, b]$:

$$
P(a \leq X \leq b) = \int_a^b f_X(x) \, dx
$$

The function $f_X$ is the **probability density function (PDF)**, and it
satisfies $\int_{-\infty}^{\infty} f_X(x) \, dx = 1$.

**In our budget model:** salaries $S_i$ and incident costs $C_{I_j}$ are continuous
(LogNormal). Overtime hours $H_i$ and incident count $I$ are discrete (Poisson).

---

## 2. Expected Value

### Definition

**Discrete case:**

$$
E[X] = \sum_{x} x \cdot p_X(x)
$$

**Continuous case:**

$$
E[X] = \int_{-\infty}^{\infty} x \, f_X(x) \, dx
$$

The expected value exists if and only if the sum (or integral) converges
absolutely.

More generally, for a function $g$ of a random variable:

$$
E[g(X)] = \int_{-\infty}^{\infty} g(x) \, f_X(x) \, dx
$$

This is the **law of the unconscious statistician (LOTUS)**.

### Theorem 2.1 — Linearity of Expectation

**Statement.** For any random variables $X$ and $Y$ (not necessarily independent)
and constants $a, b \in \mathbb{R}$:

$$
E[aX + bY] = aE[X] + bE[Y]
$$

**Proof.** We prove this for continuous random variables with joint density
$f_{X,Y}(x, y)$. The discrete case follows by replacing integrals with sums.

$$
E[aX + bY] = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} (ax + by) \, f_{X,Y}(x, y) \, dx \, dy
$$

Splitting the integral:

$$
= a \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} x \, f_{X,Y}(x, y) \, dx \, dy + b \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} y \, f_{X,Y}(x, y) \, dx \, dy
$$

The inner integral of the first term:

$$
\int_{-\infty}^{\infty} x \, f_{X,Y}(x, y) \, dy = x \, f_X(x)
$$

because $\int f_{X,Y}(x, y) \, dy = f_X(x)$ (marginalisation). Therefore:

$$
a \int_{-\infty}^{\infty} x \, f_X(x) \, dx = a \, E[X]
$$

By the same reasoning for the second term:

$$
b \int_{-\infty}^{\infty} y \, f_Y(y) \, dy = b \, E[Y]
$$

Thus:

$$
E[aX + bY] = aE[X] + bE[Y] \qquad \blacksquare
$$

**Remark.** Independence is **not** required. This is one of the most powerful
properties in probability — it holds for any random variables with finite
expectations.

**Extension to $n$ variables** (by induction):

$$
E\left[\sum_{i=1}^n a_i X_i\right] = \sum_{i=1}^n a_i \, E[X_i]
$$

**Example.** In the budget model, the expected total salary cost is:

$$
E\left[\sum_{i=1}^{50} S_i \cdot 1.80 \cdot 12\right] = \sum_{i=1}^{50} 1.80 \cdot 12 \cdot E[S_i] = 50 \times 21.6 \times E[S_i]
$$

We did not need to know whether salaries are correlated.

### Theorem 2.2 — Jensen's Inequality (Special Case)

**Statement.** For any random variable $X$ with finite second moment:

$$
E[X^2] \geq (E[X])^2
$$

**Proof.** Define $\mu = E[X]$. Consider the random variable $(X - \mu)^2 \geq 0$.
Since $(X - \mu)^2$ is non-negative:

$$
E[(X - \mu)^2] \geq 0
$$

Expanding:

$$
E[X^2 - 2\mu X + \mu^2] \geq 0
$$

By linearity of expectation:

$$
E[X^2] - 2\mu \, E[X] + \mu^2 \geq 0
$$

Since $E[X] = \mu$:

$$
E[X^2] - 2\mu^2 + \mu^2 \geq 0
$$

$$
E[X^2] - \mu^2 \geq 0
$$

$$
E[X^2] \geq (E[X])^2 \qquad \blacksquare
$$

**Consequence.** Since $\text{Var}(X) = E[X^2] - (E[X])^2$, this proves that
**variance is always non-negative**.

**Example.** For $S \sim \text{LogNormal}(9.2, 0.09)$: $E[S^2] = e^{2 \cdot 9.2 + 2 \cdot 0.09} = e^{18.58} \approx 1.18 \times 10^8$, while $(E[S])^2 = (e^{9.245})^2 = e^{18.49} \approx 1.07 \times 10^8$. Indeed $E[S^2] > (E[S])^2$.

---

## 3. Variance

### Definition

The **variance** of a random variable $X$ with mean $\mu = E[X]$ is:

$$
\text{Var}(X) = E[(X - \mu)^2]
$$

The **standard deviation** is $\text{SD}(X) = \sqrt{\text{Var}(X)}$.

### Theorem 3.1 — Computational Formula for Variance

**Statement.**

$$
\text{Var}(X) = E[X^2] - (E[X])^2
$$

**Proof.** Let $\mu = E[X]$. Expand the square in the definition:

$$
\text{Var}(X) = E[(X - \mu)^2] = E[X^2 - 2\mu X + \mu^2]
$$

By linearity of expectation:

$$
= E[X^2] - 2\mu \, E[X] + \mu^2
$$

Since $E[X] = \mu$:

$$
= E[X^2] - 2\mu^2 + \mu^2 = E[X^2] - \mu^2
$$

$$
\text{Var}(X) = E[X^2] - (E[X])^2 \qquad \blacksquare
$$

### Theorem 3.2 — Variance of a Linear Transformation

**Statement.** For constants $a, b \in \mathbb{R}$:

$$
\text{Var}(aX + b) = a^2 \, \text{Var}(X)
$$

**Proof.** Let $\mu = E[X]$, so $E[aX + b] = a\mu + b$. Then:

$$
\text{Var}(aX + b) = E[(aX + b - (a\mu + b))^2]
$$

$$
= E[(a(X - \mu))^2]
$$

$$
= E[a^2 (X - \mu)^2]
$$

$$
= a^2 \, E[(X - \mu)^2]
$$

$$
= a^2 \, \text{Var}(X) \qquad \blacksquare
$$

**Interpretation.** Adding a constant $b$ shifts the distribution but does not
change its spread. Scaling by $a$ scales the standard deviation by $|a|$ and
the variance by $a^2$.

**Example.** If $S_i$ has $\text{Var}(S_i) = \sigma_S^2$, then the annual salary
cost for one employee is $Y_i = S_i \cdot \beta \cdot 12 = 21.6 \, S_i$. So:

$$
\text{Var}(Y_i) = (21.6)^2 \, \text{Var}(S_i) = 466.56 \, \sigma_S^2
$$

---

## 4. Covariance and Independence

### Definition

The **covariance** of random variables $X$ and $Y$ is:

$$
\text{Cov}(X, Y) = E[(X - E[X])(Y - E[Y])]
$$

Expanding:

$$
\text{Cov}(X, Y) = E[XY] - E[X] \, E[Y]
$$

**Proof of the expansion:**

$$
\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]
$$

$$
= E[XY - \mu_X Y - X \mu_Y + \mu_X \mu_Y]
$$

$$
= E[XY] - \mu_X E[Y] - E[X] \mu_Y + \mu_X \mu_Y
$$

$$
= E[XY] - \mu_X \mu_Y - \mu_X \mu_Y + \mu_X \mu_Y
$$

$$
= E[XY] - E[X] \, E[Y] \qquad \blacksquare
$$

### Properties

1. $\text{Cov}(X, X) = \text{Var}(X)$
2. $\text{Cov}(X, Y) = \text{Cov}(Y, X)$ (symmetry)
3. $\text{Cov}(aX, Y) = a \, \text{Cov}(X, Y)$ (linearity)
4. If $X$ and $Y$ are independent, then $\text{Cov}(X, Y) = 0$

**Proof of property 4.** If $X \perp Y$, then $E[XY] = E[X] \, E[Y]$
(factorisation of the joint expectation). Therefore:

$$
\text{Cov}(X, Y) = E[XY] - E[X] \, E[Y] = 0 \qquad \blacksquare
$$

**Caution.** The converse is false: $\text{Cov}(X, Y) = 0$ does not imply
independence. Example: $X \sim \text{Uniform}(-1, 1)$ and $Y = X^2$. Then
$\text{Cov}(X, Y) = E[X^3] - E[X] \, E[X^2] = 0 - 0 = 0$, but $Y$ is
completely determined by $X$.

### Theorem 4.1 — Variance of a Sum

**Statement.** For any random variables $X$ and $Y$:

$$
\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)
$$

**Proof.** Let $\mu_X = E[X]$ and $\mu_Y = E[Y]$. Then $E[X + Y] = \mu_X + \mu_Y$.

$$
\text{Var}(X + Y) = E[(X + Y - \mu_X - \mu_Y)^2]
$$

$$
= E[((X - \mu_X) + (Y - \mu_Y))^2]
$$

$$
= E[(X - \mu_X)^2 + 2(X - \mu_X)(Y - \mu_Y) + (Y - \mu_Y)^2]
$$

By linearity of expectation:

$$
= E[(X - \mu_X)^2] + 2 \, E[(X - \mu_X)(Y - \mu_Y)] + E[(Y - \mu_Y)^2]
$$

$$
= \text{Var}(X) + 2\,\text{Cov}(X, Y) + \text{Var}(Y) \qquad \blacksquare
$$

**Corollary (independence).** If $X \perp Y$, then $\text{Cov}(X, Y) = 0$ and:

$$
\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)
$$

**General case for $n$ variables:**

$$
\text{Var}\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2 \sum_{i < j} \text{Cov}(X_i, X_j)
$$

If $X_1, \ldots, X_n$ are pairwise independent:

$$
\text{Var}\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i)
$$

**Example.** The total salary component $\sum_{i=1}^{50} S_i$ has variance
$50 \, \text{Var}(S_i)$ if salaries are independent. This follows directly
from the corollary above.

---

## 5. Key Distributions

### 5.1 Normal Distribution

**PDF:**

$$
f_X(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right), \quad x \in \mathbb{R}
$$

**Parameters:** $\mu \in \mathbb{R}$ (mean), $\sigma > 0$ (standard deviation).

**Moments:** $E[X] = \mu$, $\text{Var}(X) = \sigma^2$.

**Standardisation:** If $X \sim N(\mu, \sigma^2)$, then:

$$
Z = \frac{X - \mu}{\sigma} \sim N(0, 1)
$$

**Moment Generating Function:**

$$
M_X(t) = E[e^{tX}] = \exp\left(\mu t + \frac{\sigma^2 t^2}{2}\right)
$$

**Derivation of the Normal MGF.** Let $X \sim N(\mu, \sigma^2)$:

$$
M_X(t) = \int_{-\infty}^{\infty} e^{tx} \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) dx
$$

Combine the exponents:

$$
tx - \frac{(x-\mu)^2}{2\sigma^2} = -\frac{1}{2\sigma^2}\left[(x-\mu)^2 - 2\sigma^2 tx\right]
$$

Complete the square in $x$:

$$
(x-\mu)^2 - 2\sigma^2 tx = x^2 - 2(\mu + \sigma^2 t)x + \mu^2
$$

$$
= (x - (\mu + \sigma^2 t))^2 - (\mu + \sigma^2 t)^2 + \mu^2
$$

Substituting:

$$
M_X(t) = \exp\left(\frac{(\mu + \sigma^2 t)^2 - \mu^2}{2\sigma^2}\right) \int_{-\infty}^{\infty} \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - (\mu + \sigma^2 t))^2}{2\sigma^2}\right) dx
$$

The integral is 1 (it is the PDF of $N(\mu + \sigma^2 t, \sigma^2)$ integrated
over $\mathbb{R}$). The exponent simplifies:

$$
\frac{(\mu + \sigma^2 t)^2 - \mu^2}{2\sigma^2} = \frac{\mu^2 + 2\mu\sigma^2 t + \sigma^4 t^2 - \mu^2}{2\sigma^2} = \mu t + \frac{\sigma^2 t^2}{2}
$$

Therefore:

$$
M_X(t) = \exp\left(\mu t + \frac{\sigma^2 t^2}{2}\right) \qquad \blacksquare
$$

### 5.2 LogNormal Distribution

If $Y \sim N(\mu, \sigma^2)$, then $X = e^Y$ follows a **LogNormal** distribution:
$X \sim \text{LogNormal}(\mu, \sigma^2)$.

**PDF:**

$$
f_X(x) = \frac{1}{x \sigma \sqrt{2\pi}} \exp\left(-\frac{(\ln x - \mu)^2}{2\sigma^2}\right), \quad x > 0
$$

**Deriving $E[X]$ from the Normal MGF.**

Since $X = e^Y$ where $Y \sim N(\mu, \sigma^2)$:

$$
E[X] = E[e^Y] = M_Y(1)
$$

where $M_Y(t) = \exp(\mu t + \sigma^2 t^2 / 2)$ is the MGF of $Y$. Setting $t = 1$:

$$
E[X] = \exp\left(\mu + \frac{\sigma^2}{2}\right) \qquad \blacksquare
$$

**Deriving $E[X^2]$.**

$$
E[X^2] = E[e^{2Y}] = M_Y(2) = \exp\left(2\mu + \frac{4\sigma^2}{2}\right) = \exp(2\mu + 2\sigma^2)
$$

**Deriving $\text{Var}(X)$.**

$$
\text{Var}(X) = E[X^2] - (E[X])^2 = e^{2\mu + 2\sigma^2} - e^{2\mu + \sigma^2}
$$

$$
= e^{2\mu + \sigma^2}\left(e^{\sigma^2} - 1\right) \qquad \blacksquare
$$

**Numerical example** (salary: $\mu_s = 9.2$, $\sigma_s = 0.3$, so $\sigma_s^2 = 0.09$):

$$
E[S_i] = e^{9.2 + 0.045} = e^{9.245} \approx 10{,}362.02
$$

$$
\text{Var}(S_i) = e^{18.4 + 0.09}(e^{0.09} - 1) = e^{18.49} \times 0.09417 \approx 10{,}117{,}947
$$

$$
\text{SD}(S_i) = \sqrt{10{,}117{,}947} \approx 3{,}180.87
$$

**Interpretation.** The monthly salary distribution is centered around
R\$ 10,362 with a standard deviation of about R\$ 3,181. The right-skew of the
LogNormal means a few employees earn significantly more than the mean.

### 5.3 Poisson Distribution

A discrete random variable $X$ follows a **Poisson** distribution with parameter
$\lambda > 0$ if:

**PMF:**

$$
p_X(k) = P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \ldots
$$

**Deriving $E[X]$ from the definition.**

$$
E[X] = \sum_{k=0}^{\infty} k \cdot \frac{\lambda^k e^{-\lambda}}{k!}
$$

The $k = 0$ term is zero. For $k \geq 1$:

$$
= \sum_{k=1}^{\infty} k \cdot \frac{\lambda^k e^{-\lambda}}{k!}
= \sum_{k=1}^{\infty} \frac{\lambda^k e^{-\lambda}}{(k-1)!}
$$

Substituting $j = k - 1$:

$$
= \lambda e^{-\lambda} \sum_{j=0}^{\infty} \frac{\lambda^j}{j!}
= \lambda e^{-\lambda} \cdot e^{\lambda}
= \lambda \qquad \blacksquare
$$

**Deriving $E[X^2]$.**

We first compute $E[X(X-1)]$:

$$
E[X(X-1)] = \sum_{k=2}^{\infty} k(k-1) \cdot \frac{\lambda^k e^{-\lambda}}{k!}
= \sum_{k=2}^{\infty} \frac{\lambda^k e^{-\lambda}}{(k-2)!}
$$

Substituting $j = k - 2$:

$$
= \lambda^2 e^{-\lambda} \sum_{j=0}^{\infty} \frac{\lambda^j}{j!}
= \lambda^2
$$

Therefore:

$$
E[X^2] = E[X(X-1)] + E[X] = \lambda^2 + \lambda
$$

**Deriving $\text{Var}(X)$:**

$$
\text{Var}(X) = E[X^2] - (E[X])^2 = \lambda^2 + \lambda - \lambda^2 = \lambda \qquad \blacksquare
$$

**Key property:** For Poisson, the mean equals the variance.

**Numerical examples:**

- Overtime hours: $H_i \sim \text{Poisson}(5)$. So $E[H_i] = 5$ and $\text{Var}(H_i) = 5$.
- Incidents: $I \sim \text{Poisson}(3)$. So $E[I] = 3$ and $\text{Var}(I) = 3$.

---

## 6. Moment Generating Functions

### Definition

The **moment generating function (MGF)** of a random variable $X$ is:

$$
M_X(t) = E[e^{tX}]
$$

defined for all $t$ in a neighbourhood of zero where the expectation exists.

### Key Properties

1. **Moment extraction:** $E[X^n] = M_X^{(n)}(0)$ (the $n$-th derivative
   evaluated at $t = 0$).

2. **Uniqueness theorem:** If $M_X(t) = M_Y(t)$ for all $t$ in a neighbourhood
   of zero, then $X$ and $Y$ have the same distribution.

3. **Sum of independents:** If $X \perp Y$, then $M_{X+Y}(t) = M_X(t) \cdot M_Y(t)$.

**Proof of property 3:**

$$
M_{X+Y}(t) = E[e^{t(X+Y)}] = E[e^{tX} \cdot e^{tY}]
$$

By independence, $E[e^{tX} \cdot e^{tY}] = E[e^{tX}] \cdot E[e^{tY}]$:

$$
= M_X(t) \cdot M_Y(t) \qquad \blacksquare
$$

**Why MGFs matter for this project:** The MGF approach is how we will prove the
Central Limit Theorem in Phase 3. The idea is: show that the MGF of the
standardised sum converges to $e^{t^2/2}$ (the MGF of the standard Normal).
By the uniqueness theorem, this implies convergence in distribution.

---

## 7. Analytical Moments of the Budget Model

### Model Recap

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} S_i \cdot \beta \cdot 12}_{\text{Term 1}} + \underbrace{\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12}_{\text{Term 2}} + \underbrace{\sum_{j=1}^{I} C_{I_j}}_{\text{Term 3}}
$$

**Assumptions:** $S_i$ are i.i.d., $H_i$ are i.i.d., $C_{I_j}$ are i.i.d.,
and Terms 1, 2, 3 are mutually independent.

### 7.1 Expected Value: $E[X_{\text{total}}]$

By linearity of expectation (Theorem 2.1):

$$
E[X_{\text{total}}] = E[\text{Term 1}] + E[\text{Term 2}] + E[\text{Term 3}]
$$

**Term 1: Salary + Benefits**

$$
E[\text{Term 1}] = E\left[\sum_{i=1}^{n} S_i \cdot \beta \cdot 12\right]
= \sum_{i=1}^{n} \beta \cdot 12 \cdot E[S_i]
= n \cdot \beta \cdot 12 \cdot E[S_i]
$$

With $S_i \sim \text{LogNormal}(9.2, 0.09)$:

$$
E[S_i] = e^{9.2 + 0.045} = e^{9.245} \approx 10{,}362.02
$$

$$
E[\text{Term 1}] = 50 \times 1.80 \times 12 \times 10{,}362.02 = 1080 \times 10{,}362.02 \approx 11{,}190{,}982
$$

**Term 2: Regular Overtime**

$$
E[\text{Term 2}] = E\left[\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12\right]
= n \cdot r_{ot} \cdot 12 \cdot E[H_i]
$$

With $H_i \sim \text{Poisson}(5)$:

$$
E[\text{Term 2}] = 50 \times 80 \times 12 \times 5 = 240{,}000
$$

**Term 3: Incident Costs**

Term 3 is a **random sum**: $\sum_{j=1}^{I} C_{I_j}$ where $I \sim \text{Poisson}(\lambda_I)$ and
$C_{I_j} \sim \text{LogNormal}(\mu_I, \sigma_I^2)$ are i.i.d. and independent
of $I$.

By the **law of total expectation** (Wald's equation):

$$
E\left[\sum_{j=1}^{I} C_{I_j}\right] = E[I] \cdot E[C_{I_j}]
$$

This requires: (a) $I$ and $C_{I_j}$ are independent, and (b) $C_{I_j}$ are
i.i.d. Both hold by model assumption.

$$
E[C_{I_j}] = e^{10.5 + 0.125} = e^{10.625} \approx 41{,}171.16
$$

$$
E[\text{Term 3}] = 3 \times 41{,}171.16 \approx 123{,}513
$$

**Total:**

$$
E[X_{\text{total}}] \approx 11{,}190{,}982 + 240{,}000 + 123{,}513 \approx R\$ \, 11{,}554{,}495
$$

### 7.2 Variance: $\text{Var}(X_{\text{total}})$

By independence of Terms 1, 2, 3 (Theorem 4.1 corollary):

$$
\text{Var}(X_{\text{total}}) = \text{Var}(\text{Term 1}) + \text{Var}(\text{Term 2}) + \text{Var}(\text{Term 3})
$$

**Term 1:**

$$
\text{Var}(\text{Term 1}) = \text{Var}\left(\sum_{i=1}^{n} \beta \cdot 12 \cdot S_i\right)
= (\beta \cdot 12)^2 \sum_{i=1}^{n} \text{Var}(S_i)
= n \cdot (\beta \cdot 12)^2 \cdot \text{Var}(S_i)
$$

With:

$$
\text{Var}(S_i) = e^{2 \cdot 9.2 + 0.09}(e^{0.09} - 1) = e^{18.49} \times 0.09417 \approx 10{,}117{,}947
$$

$$
\text{Var}(\text{Term 1}) = 50 \times (21.6)^2 \times 10{,}117{,}947 = 50 \times 466.56 \times 10{,}117{,}947
$$

$$
\approx 2.360 \times 10^{11}
$$

**Term 2:**

$$
\text{Var}(\text{Term 2}) = n \cdot (r_{ot} \cdot 12)^2 \cdot \text{Var}(H_i)
$$

With $\text{Var}(H_i) = \lambda_h = 5$:

$$
\text{Var}(\text{Term 2}) = 50 \times (960)^2 \times 5 = 50 \times 921{,}600 \times 5 = 230{,}400{,}000
$$

$$
\approx 2.304 \times 10^{8}
$$

**Term 3 (compound Poisson):**

For a compound Poisson sum $\sum_{j=1}^I C_j$ where $I \sim \text{Poisson}(\lambda)$
and $C_j$ are i.i.d. with $E[C] = \mu_C$ and $\text{Var}(C) = \sigma_C^2$:

$$
\text{Var}\left(\sum_{j=1}^I C_j\right) = \lambda \cdot E[C^2] = \lambda \cdot (\sigma_C^2 + \mu_C^2)
$$

**Derivation** (via law of total variance):

$$
\text{Var}\left(\sum C_j\right) = E\left[\text{Var}\left(\sum C_j \mid I\right)\right] + \text{Var}\left(E\left[\sum C_j \mid I\right]\right)
$$

$$
= E[I \cdot \sigma_C^2] + \text{Var}(I \cdot \mu_C)
$$

$$
= \lambda \sigma_C^2 + \mu_C^2 \lambda
$$

$$
= \lambda(\sigma_C^2 + \mu_C^2) = \lambda \cdot E[C^2]
$$

With $C_{I_j} \sim \text{LogNormal}(10.5, 0.25)$:

$$
E[C^2] = e^{2 \cdot 10.5 + 2 \cdot 0.25} = e^{21.5} \approx 2{,}174{,}823{,}009
$$

$$
\text{Var}(\text{Term 3}) = 3 \times 2{,}174{,}823{,}009 \approx 6.525 \times 10^{9}
$$

**Total:**

$$
\text{Var}(X_{\text{total}}) \approx 2.360 \times 10^{11} + 2.304 \times 10^{8} + 6.525 \times 10^{9}
$$

$$
\approx 2.428 \times 10^{11}
$$

$$
\text{SD}(X_{\text{total}}) \approx \sqrt{2.428 \times 10^{11}} \approx R\$ \, 492{,}747
$$

### 7.3 Summary of Analytical Moments

| Quantity | Value |
|----------|-------|
| $E[X_{\text{total}}]$ | $\approx R\$ \, 11{,}554{,}495$ |
| $\text{Var}(X_{\text{total}})$ | $\approx 2.428 \times 10^{11}$ |
| $\text{SD}(X_{\text{total}})$ | $\approx R\$ \, 492{,}747$ |

**Interpretation.** The expected total annual cost is roughly R\$ 11.55M, with a
standard deviation of about R\$ 493K. The salary component (Term 1) dominates
both the expected value ($\sim 97\%$) and the variance ($\sim 97\%$). This
suggests that uncertainty in salaries is the primary driver of budget risk.

**What Monte Carlo adds:** These analytical moments give us $E[X]$ and $\text{Var}(X)$,
but they do **not** give us:

- The full shape of the distribution (skewness, tail behaviour)
- $P(X > B)$ for a budget ceiling $B$ (overbudget probability)
- Exact confidence intervals (these require the CLT, Phase 3)
- The effect of changing distributional assumptions

Monte Carlo simulation will recover these moments **and** provide the full
distribution $F_X$ — answering questions that analytical methods alone cannot.
