# Exercises — Phase 5: Variance Reduction Techniques

Solve on paper. These exercises prove variance reduction formulas and
apply them to the budget model.

---

## Proofs (paper)

### Exercise 1 — Antithetic Variate Variance

**Prove** that the antithetic variate estimator

$$
\hat{\mu}_{AV} = \frac{1}{N/2} \sum_{i=1}^{N/2} \frac{g(X_i) + g(X_i')}{2}
$$

has variance:

$$
\text{Var}(\hat{\mu}_{AV}) = \frac{1}{N}\left[\text{Var}(g(X)) + \text{Cov}(g(X), g(X'))\right]
$$

*Expand the variance of the average of paired terms. Use the fact that
pairs are i.i.d. but within each pair, $X_i$ and $X_i'$ are correlated.*

---

### Exercise 2 — Optimal Control Variate Coefficient

**Derive** the optimal control variate coefficient:

$$
c^* = \frac{\text{Cov}(g(X), h(X))}{\text{Var}(h(X))}
$$

by minimising $\text{Var}(\hat{\mu}_{CV})$ with respect to $c$.

*Take the derivative of
$\text{Var}(g - ch) = \text{Var}(g) - 2c\,\text{Cov}(g,h) + c^2\,\text{Var}(h)$
with respect to $c$, set to zero, and verify the second-order condition.*

---

### Exercise 3 — Variance at Optimal $c^*$

**Prove** that at $c = c^*$:

$$
\text{Var}(\hat{\mu}_{CV}^*) = \frac{\text{Var}(g(X))}{N}(1 - \rho_{g,h}^2)
$$

*Substitute $c^*$ back into the variance formula from Exercise 2.
Factor out $\text{Var}(g)/N$ and recognise $\rho^2$.*

**Interpret:** What happens as $\rho^2 \to 1$? When is control variates
most effective? When is it useless ($\rho = 0$)?

---

### Exercise 4 — Stratified Sampling Never Increases Variance

**Prove** that:

$$
\text{Var}(\hat{\mu}_{SS}) \leq \text{Var}(\hat{\mu}_{MC})
$$

*Use the law of total variance:
$\text{Var}(g) = E[\text{Var}(g|A)] + \text{Var}(E[g|A])$.
Show that stratified sampling removes the $\text{Var}(E[g|A])$ term,
which is always $\geq 0$.*

---

## Computations (paper)

### Exercise 5 — Control Variate Efficiency

In the budget model, $g(X)$ is the total cost and
$h(X) = \sum_{i=1}^{50} S_i$ (total raw salaries). You estimate
$\rho_{g,h} = 0.92$.

1. What is the variance reduction factor $(1 - \rho^2)$?
2. How many **naive MC** samples would achieve the same precision as
   $N = 1{,}000$ control variate samples?
3. If $\rho$ improves to 0.98 (e.g., by using a better control variate),
   how does the answer change?

---

### Exercise 6 — Stratified Sampling Computation

You partition the salary distribution into 3 strata:

| Stratum | Range | Proportion $p_k$ | Within-stratum variance $\sigma_k^2$ |
|---------|-------|-------------------|--------------------------------------|
| Low | $S < 8K$ | 0.20 | $1.2 \times 10^6$ |
| Medium | $8K \leq S < 15K$ | 0.60 | $0.8 \times 10^6$ |
| High | $S \geq 15K$ | 0.20 | $3.5 \times 10^6$ |

The overall variance is $\sigma^2 = 2.1 \times 10^6$.

1. Compute $\text{Var}(\hat{\mu}_{SS}) = \frac{1}{N}\sum_k p_k \sigma_k^2$.
2. Compare to naive MC: $\text{Var}(\hat{\mu}_{MC}) = \sigma^2 / N$.
3. What is the variance reduction factor?
4. Compute the between-strata variance $\sum_k p_k(\mu_k - \mu)^2$ and
   verify it equals $\sigma^2 - \sum_k p_k \sigma_k^2$.
