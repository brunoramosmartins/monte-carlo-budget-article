# Exercises — Phase 3: Central Limit Theorem and Confidence Intervals

Solve on paper. These exercises reinforce the CLT proof, CI derivation,
and the practical question of choosing $N$ for Monte Carlo.

---

## Proofs (paper)

### Exercise 1 — Derive the Normal MGF

**Derive** the MGF of $X \sim N(\mu, \sigma^2)$:

$$
M_X(t) = \exp\left(\mu t + \frac{\sigma^2 t^2}{2}\right)
$$

*Complete the square in the integral:*

$$
M_X(t) = \int_{-\infty}^{\infty} e^{tx} \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) dx
$$

*Combine the exponents $tx - (x-\mu)^2/(2\sigma^2)$, complete the square
in $x$, and recognise the resulting integral as a Normal PDF integrated
over $\mathbb{R}$ (which equals 1).*

---

### Exercise 2 — Prove the CLT (MGF Approach)

**Prove** the Central Limit Theorem using the MGF approach for i.i.d. variables
$X_1, \ldots, X_n$ with $E[X_i] = \mu$, $\text{Var}(X_i) = \sigma^2$, and
finite third moment.

Show all steps explicitly:

1. Define $W_i = (X_i - \mu)/\sigma$ and verify $E[W_i] = 0$, $\text{Var}(W_i) = 1$.
2. Express $Z_n = \sqrt{n}(\bar{X}_n - \mu)/\sigma$ in terms of $W_i$.
3. Factor $M_{Z_n}(t) = [M_W(t/\sqrt{n})]^n$ using independence.
4. Taylor expand $M_W(s) = 1 + s^2/2 + O(s^3)$ using the moments of $W$.
5. Take $\log$: $\log M_W(s) = s^2/2 + O(s^3)$.
6. Substitute $s = t/\sqrt{n}$ and multiply by $n$.
7. Show the remainder vanishes: $n \cdot O(t^3/n^{3/2}) = O(t^3/\sqrt{n}) \to 0$.
8. Conclude $M_{Z_n}(t) \to e^{t^2/2}$ and invoke uniqueness.

---

### Exercise 3 — From Variance to Distribution

**Prove** that the Monte Carlo standard error $\text{SE} = \sigma / \sqrt{N}$
follows directly from $\text{Var}(\bar{X}_N) = \sigma^2 / N$.

Then explain: how does the CLT **upgrade** this from a variance statement
to a distributional statement?

*Specifically: the WLLN + Chebyshev gives
$P(|\bar{X}_N - \mu| \geq \epsilon) \leq \sigma^2/(N\epsilon^2)$
(a bound). The CLT gives
$P(|\bar{X}_N - \mu| \geq \epsilon) \approx 2[1 - \Phi(\epsilon\sqrt{N}/\sigma)]$
(an approximation). Why is the CLT result more useful in practice?*

---

### Exercise 4 — Derive the Minimum $N$ Formula

**Derive** the formula:

$$
N \geq \left(\frac{z_{\alpha/2} \cdot \sigma}{\epsilon}\right)^2
$$

for the minimum number of simulations needed to achieve a confidence interval
of half-width $\epsilon$ at confidence level $1 - \alpha$.

*Start from the CLT approximation
$P(|\bar{X}_N - \mu| \leq \epsilon) \approx 1 - \alpha$
and solve for $N$.*

---

## Computations (paper)

### Exercise 5 — Confidence Intervals at Multiple Levels

You run a Monte Carlo budget simulation with $N = 5{,}000$ iterations.
Results: $\bar{X} = 12{,}500{,}000$ and $s = 480{,}000$.

**Compute** the 90%, 95%, and 99% confidence intervals for $E[X_{\text{total}}]$.

*Use $z_{0.05} = 1.645$, $z_{0.025} = 1.960$, $z_{0.005} = 2.576$.*

---

### Exercise 6 — Required $N$ for a CFO's Precision

Your CFO wants the budget estimate to be within $\pm R\$ \, 50{,}000$ of the
true mean with 95% confidence. A pilot run with $N = 100$ gave
$s = 600{,}000$.

1. How many simulations do you need?
2. If the CFO then asks for $\pm R\$ \, 25{,}000$, how does $N$ change?
3. Comment on the scaling law $N \propto 1/\epsilon^2$.

---

### Exercise 7 — Berry-Esseen Application

For standardised salary costs, assume $E[|W|^3] = \rho / \sigma^3 = 2.5$.

1. Compute the Berry-Esseen bound on
   $\sup_x |F_{\bar{Z}_n}(x) - \Phi(x)|$ for $n = 30$ and $n = 100$.
   Use $C = 0.4748$.

2. Is the Normal approximation reasonable at $n = 30$? At $n = 100$?

3. In the budget model, each simulation sums over $n = 50$ employees.
   Does this help or hurt the Normal approximation for $X_{\text{total}}$?
