# Exercises — Phase 4: Monte Carlo Method

Solve on paper. These exercises connect the Monte Carlo estimator to the
theorems from Phases 1–3 and build practical intuition.

---

## Proofs (paper)

### Exercise 1 — Unbiasedness

**Prove** that the Monte Carlo estimator
$\hat{\mu}_N = \frac{1}{N} \sum_{i=1}^N g(X_i)$ is unbiased for
$\theta = E[g(X)]$.

*Use linearity of expectation. State what "i.i.d." gives you.*

---

### Exercise 2 — Consistency

**Prove** that $\hat{\mu}_N$ is a consistent estimator of $\theta = E[g(X)]$.

*State which LLN version you are using (Weak or Strong) and verify that its
conditions are satisfied. Explicitly connect to Phase 2, Theorem 3.1.*

---

### Exercise 3 — Dimension-Free Convergence

**Prove** that the Monte Carlo convergence rate is $O(1/\sqrt{N})$,
independent of the dimension of $X$.

*Start from $\text{SE} = \sigma_g / \sqrt{N}$. Contrast with the trapezoidal
rule in $d$ dimensions, which has rate $O(N^{-2/d})$. For what dimension $d$
does the trapezoidal rule match Monte Carlo's rate? Interpret.*

---

### Exercise 4 — MSE Decomposition

**Show** that the mean squared error of the MC estimator satisfies:

$$
\text{MSE}(\hat{\mu}_N) = \frac{\text{Var}(g(X))}{N}
$$

*Use the bias-variance decomposition:
$\text{MSE} = \text{Bias}^2 + \text{Var}$.
Since the estimator is unbiased, what remains?*

---

## Computations (paper)

### Exercise 5 — Budget CI and Overbudget Probability

You simulate a budget 10,000 times and obtain $\bar{X} = 12{,}450{,}000$
and $s = 520{,}000$.

1. Compute the 95% confidence interval for $E[X_{\text{total}}]$.
2. If the budget ceiling is R\$ 13,000,000, estimate
   $P(X > 13{,}000{,}000)$ assuming the individual simulation outputs
   are approximately Normal. *Hint: standardise and use $\Phi$.*
3. What is the Monte Carlo standard error of your estimate?

---

### Exercise 6 — Scaling Law

To halve the CI width from $\pm R\$ \, 100K$ to $\pm R\$ \, 50K$:

1. How many additional simulations are needed if the current run used
   $N = 1{,}000$?
2. Derive the general scaling law: if the current CI half-width is $\epsilon$
   with $N$ simulations, how many simulations $N'$ are needed for
   half-width $\epsilon' = \epsilon / k$?
3. Plot $N$ vs $\epsilon$ for $\epsilon \in [10K, 500K]$ with $\sigma = 500K$
   and 95% confidence. What shape is the curve?
