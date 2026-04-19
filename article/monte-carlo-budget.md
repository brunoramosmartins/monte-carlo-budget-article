# Why Your Budget Never Hits the Exact Number

## Monte Carlo Simulation for IT Budget Planning — from Point Estimates to Probability Distributions

---

## 1. Introduction

Your CFO asks for next year's IT headcount budget. You open a spreadsheet, multiply headcount by average salary, add a benefits multiplier, toss in an overtime estimate, round up for incidents — and deliver a number. A single number. R$ 11.5 million.

But what if that number is just one sample from a distribution you have never seen?

Every organisation that manages headcount budgets — salaries, benefits, overtime, unplanned costs — faces the same ritual. The team produces a point estimate, leadership approves it, and the year unfolds. Months later, during a Forecast Year-end Financial (FYF) review, the actual spending deviates from the forecast. The team adjusts. Another review. Another adjustment. By year-end, the original number looks like little more than an educated guess.

The problem is not that the estimate was wrong. The problem is that a single number carries no information about its own uncertainty. Was R$ 11.5M a conservative estimate? An optimistic one? How likely are we to exceed R$ 12.5M? The point estimate cannot answer these questions — because it discards everything except the centre of the distribution.

This article replaces the single number with a **probability distribution**. Using Monte Carlo simulation grounded in the Law of Large Numbers and the Central Limit Theorem, we transform "we expect to spend R$ 11.5M" into "we are 90% confident spending will fall between R$ 10.7M and R$ 12.4M, with a 7% probability of exceeding the R$ 12.5M ceiling."

The mathematical journey proceeds in four stages: we formalise the budget components as random variables (Section 3), prove that averaging simulations converges to the true answer (Section 4), quantify the simulation error (Section 5), and implement the estimator with variance reduction techniques (Sections 6–7). Section 9 validates everything experimentally.

### Notation

Throughout this article, we use the following notation:

| Symbol | Meaning |
|--------|---------|
| $S_i$ | Monthly salary of employee $i$ |
| $\beta$ | Benefits multiplier (encargos) |
| $n$ | Number of employees (headcount) |
| $H_i$ | Overtime hours per employee per month |
| $r_{ot}$ | Overtime hourly rate |
| $I$ | Number of severe incidents per year |
| $C_j$ | Cost of incident $j$ |
| $X_{\text{total}}$ | Total annual budget cost |
| $\bar{X}_N$ | Sample mean of $N$ simulations |
| $\hat{\theta}_N$ | Monte Carlo estimator |

---

## 2. The Point Estimate Problem

A point estimate is a single value used to approximate an unknown parameter. In budget planning, it takes the form:

$$
\hat{X} = n \times \bar{S} \times \beta \times 12 + \text{overtime} + \text{incidents}
$$

where $\bar{S}$ is the average salary and everything else is a constant. The result is a number — say, R$ 11,554,473.

But this number is $E[X_{\text{total}}]$: the expected value of a random variable. It tells us the centre of the distribution. What it discards is everything else:

- **Variance:** How spread out are the possible outcomes?
- **Skewness:** Is the distribution symmetric, or could costs be pulled much higher by a few extreme salaries?
- **Tail risk:** What is the probability of exceeding the approved budget?
- **Confidence:** How sure are we that the true cost is within ±R$ 500K of our estimate?

In formal terms, the point estimate gives us $E[X]$ but not the distribution $F_X$. Monte Carlo simulation recovers $F_X$ — the full picture.

---

## 3. Random Variables in Disguise

Every component of the budget is a random variable. Treating them as constants is a modelling choice that discards information.

### Salaries: LogNormal

Salaries in a mixed-seniority IT team are strictly positive and right-skewed: most employees earn near the median, but a few senior engineers or managers earn significantly more. The LogNormal distribution captures this:

$$
S_i \sim \text{LogNormal}(\mu_s, \sigma_s^2)
$$

With parameters $\mu_s = 9.2$ and $\sigma_s = 0.3$, the expected monthly salary is:

$$
E[S_i] = e^{\mu_s + \sigma_s^2/2} = e^{9.245} \approx R\$ \, 10{,}362
$$

The variance is:

$$
\text{Var}(S_i) = (e^{\sigma_s^2} - 1) \cdot e^{2\mu_s + \sigma_s^2} \approx 10{,}117{,}947
$$

### Overtime: Poisson

Overtime hours per employee per month are discrete, non-negative, and relatively rare — a natural fit for the Poisson distribution:

$$
H_i \sim \text{Poisson}(\lambda_h), \quad \lambda_h = 5
$$

A key property: for Poisson, $E[H_i] = \text{Var}(H_i) = \lambda_h$.

### Incidents: Compound Poisson

Severe incidents — outages, security breaches, emergency deployments — occur at a random rate with random severity:

$$
I \sim \text{Poisson}(\lambda_I), \quad C_j \sim \text{LogNormal}(\mu_I, \sigma_I^2)
$$

The total incident cost is a **random sum of random variables**: $\sum_{j=1}^I C_j$.

### The Total Cost Model

Combining all components:

$$
X_{\text{total}} = \underbrace{\sum_{i=1}^{n} S_i \cdot \beta \cdot 12}_{\text{salaries + benefits}} + \underbrace{\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12}_{\text{overtime}} + \underbrace{\sum_{j=1}^{I} C_j}_{\text{incidents}}
$$

Using linearity of expectation (which holds regardless of independence):

$$
E[X_{\text{total}}] = n \cdot \beta \cdot 12 \cdot E[S_i] + n \cdot r_{ot} \cdot 12 \cdot E[H_i] + E[I] \cdot E[C_j]
$$

With default parameters ($n = 50$, $\beta = 1.80$, $r_{ot} = 80$, $\lambda_I = 3$):

$$
E[X_{\text{total}}] \approx 11{,}191{,}000 + 240{,}000 + 123{,}500 \approx R\$ \, 11{,}554{,}500
$$

The salary component dominates at ~97% of the total. This will matter for variance reduction later.

---

## 4. Will the Mean Converge? The Law of Large Numbers

If we simulate the budget 10,000 times and average the results, will the average converge to the true $E[X_{\text{total}}]$? The Law of Large Numbers says yes.

### Chebyshev's Inequality

For any random variable $X$ with mean $\mu$ and variance $\sigma^2$:

$$
P(|X - \mu| \geq \epsilon) \leq \frac{\sigma^2}{\epsilon^2}
$$

This is derived from Markov's inequality applied to $(X - \mu)^2$.

### The Weak Law of Large Numbers

Let $X_1, \ldots, X_N$ be i.i.d. with mean $\mu$ and variance $\sigma^2$. The sample mean $\bar{X}_N = \frac{1}{N}\sum X_i$ satisfies:

$$
P(|\bar{X}_N - \mu| \geq \epsilon) \leq \frac{\sigma^2}{N\epsilon^2} \to 0 \quad \text{as } N \to \infty
$$

**Proof.** Since $E[\bar{X}_N] = \mu$ and $\text{Var}(\bar{X}_N) = \sigma^2/N$, applying Chebyshev to $\bar{X}_N$ gives the result immediately. $\blacksquare$

The Strong Law of Large Numbers provides an even stronger guarantee: $\bar{X}_N \to \mu$ almost surely, meaning the convergence happens with probability 1, not just in probability.

**For Monte Carlo:** each simulation $X_i$ is one "possible year." The LLN guarantees that averaging $N$ simulated years converges to the true expected cost. Figure 1 demonstrates this visually.

![LLN Convergence](../figures/lln_convergence.png)
*Figure 1: Ten independent runs of the sample mean converging to $E[S]$, with Chebyshev 95% confidence band.*

---

## 5. How Wrong Can We Be? The Central Limit Theorem

The LLN tells us the estimate converges. The CLT tells us **how fast** — and gives us confidence intervals.

### Statement

For i.i.d. variables with mean $\mu$ and variance $\sigma^2$:

$$
\frac{\sqrt{N}(\bar{X}_N - \mu)}{\sigma} \xrightarrow{d} N(0, 1)
$$

### Proof Sketch (MGF Approach)

Define $W_i = (X_i - \mu)/\sigma$ so that $E[W_i] = 0$ and $\text{Var}(W_i) = 1$. The standardised sum is $Z_N = \frac{1}{\sqrt{N}}\sum W_i$. Its MGF is:

$$
M_{Z_N}(t) = \left[M_W\left(\frac{t}{\sqrt{N}}\right)\right]^N
$$

Taylor expanding $\log M_W(s) = s^2/2 + O(s^3)$ and substituting $s = t/\sqrt{N}$:

$$
\log M_{Z_N}(t) = N \cdot \left[\frac{t^2}{2N} + O\left(\frac{t^3}{N^{3/2}}\right)\right] = \frac{t^2}{2} + O\left(\frac{t^3}{\sqrt{N}}\right) \to \frac{t^2}{2}
$$

Since $e^{t^2/2}$ is the MGF of $N(0, 1)$, the uniqueness theorem gives $Z_N \xrightarrow{d} N(0, 1)$. $\blacksquare$

### Confidence Intervals

From the CLT, the $(1-\alpha)$ confidence interval for $\mu$ is:

$$
\bar{X}_N \pm z_{\alpha/2} \cdot \frac{s_N}{\sqrt{N}}
$$

where $s_N$ is the sample standard deviation and $z_{\alpha/2}$ is the Normal quantile (1.96 for 95%).

### Choosing N

To achieve a CI half-width of $\epsilon$:

$$
N \geq \left(\frac{z_{\alpha/2} \cdot \sigma}{\epsilon}\right)^2
$$

For our budget ($\sigma \approx 493K$, $\epsilon = 100K$, 95% confidence): $N \geq (1.96 \times 493{,}000 / 100{,}000)^2 \approx 94$. The CLT is remarkably efficient.

![CLT Normality Emergence](../figures/clt_normality_emergence.png)
*Figure 2: As $n$ increases, the standardised mean of LogNormal salaries converges to $N(0,1)$.*

---

## 6. The Monte Carlo Estimator

### Definition

The Monte Carlo estimator of $\theta = E[g(X)]$ is:

$$
\hat{\theta}_N = \frac{1}{N} \sum_{i=1}^N g(X_i)
$$

where each $g(X_i)$ is the total cost from one simulated year.

### Properties

**Unbiasedness.** $E[\hat{\theta}_N] = \frac{1}{N}\sum E[g(X_i)] = \theta$. The estimator has no systematic bias.

**Consistency.** By the WLLN: $\hat{\theta}_N \xrightarrow{P} \theta$. More simulations means more accuracy.

**Asymptotic normality.** By the CLT: $\sqrt{N}(\hat{\theta}_N - \theta)/\sigma_g \xrightarrow{d} N(0, 1)$. We can build confidence intervals.

**Convergence rate.** The standard error is $\text{SE} = \sigma_g / \sqrt{N}$, which decays as $O(1/\sqrt{N})$. Crucially, this rate is **independent of the dimension** of $X$ — unlike deterministic integration methods that suffer from the curse of dimensionality.

### The Scaling Law

Halving the CI width requires 4× more simulations. Going from ±R$ 100K to ±R$ 50K means quadrupling $N$. This fundamental trade-off motivates variance reduction.

### Mean Squared Error

Since the estimator is unbiased:

$$
\text{MSE}(\hat{\theta}_N) = \text{Var}(\hat{\theta}_N) = \frac{\sigma_g^2}{N}
$$

---

## 7. Making It Faster: Variance Reduction

The $O(1/\sqrt{N})$ rate means brute-force precision is expensive. Variance reduction techniques achieve tighter confidence intervals **for the same computational budget**.

### Control Variates

If we know $E[h(X)]$ analytically for some function $h$ correlated with $g$, we can correct our estimate:

$$
\hat{\theta}_{CV} = \hat{\theta}_N - c^*\left(\bar{h}_N - E[h(X)]\right)
$$

The optimal coefficient minimises variance:

$$
c^* = \frac{\text{Cov}(g(X), h(X))}{\text{Var}(h(X))}
$$

At this optimal $c^*$, the variance becomes:

$$
\text{Var}(\hat{\theta}_{CV}) = \frac{\text{Var}(g(X))}{N}(1 - \rho_{g,h}^2)
$$

where $\rho_{g,h}$ is the correlation between $g$ and $h$.

**For our budget model:** using $h(X) = \sum S_i$ (total raw salaries, with known analytical mean) as the control variate yields $\rho \approx 0.99$, reducing variance by a factor of ~$(1 - 0.99^2) \approx 0.02$ — roughly a **50× improvement**.

### Antithetic Variates

Generate pairs $(X_i, X_i')$ where $X_i' = F^{-1}(1 - F(X_i))$ is the "mirror" of $X_i$. The estimator uses pair-wise averages:

$$
\hat{\theta}_{AV} = \frac{1}{N/2}\sum_{i=1}^{N/2} \frac{g(X_i) + g(X_i')}{2}
$$

If $g$ is monotone, $\text{Cov}(g(X), g(X')) < 0$, and variance is reduced.

### Stratified Sampling

Partition the input space into $K$ strata, sample proportionally within each, and combine. By the law of total variance:

$$
\text{Var}(\hat{\theta}_{SS}) = \frac{1}{N}\sum_k p_k \sigma_k^2 \leq \frac{\sigma^2}{N} = \text{Var}(\hat{\theta}_{MC})
$$

Stratification removes the between-strata variance, which is always non-negative.

![Variance Reduction Comparison](../figures/variance_reduction_comparison.png)
*Figure 3: CI width vs N for naive MC, antithetic variates, and control variates. Control variates dominate.*

---

## 8. A Bayesian Alternative

The frequentist Monte Carlo approach assumes a fixed model and simulates from it. The Bayesian approach treats unknown parameters as random variables and updates beliefs as data arrives:

$$
P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \cdot P(\theta)
$$

In the budget context: the **prior** is last year's cost distribution, the **likelihood** is this year's spending data, and the **posterior** is the updated forecast. Each FYF review is, in practice, informal Bayesian updating.

| Aspect | Frequentist MC | Bayesian |
|--------|---------------|----------|
| Parameters | Fixed constants | Random variables |
| Prior information | Not used | Explicitly encoded |
| Output | Confidence interval | Credible interval |
| Interpretation | Long-run frequency | Probability about $\theta$ |
| Mid-year updating | Requires re-specification | Natural (posterior → new prior) |

This article uses the frequentist approach for its generality (no prior elicitation needed), pedagogical clarity, and practical simplicity. The Bayesian extension is a natural next step for teams with historical budget data.

---

## 9. Experiments and Results

### Experiment A: LLN Convergence

Ten independent runs of the salary sample mean converge to $E[S]$ as $N$ grows (Figure 1). At small $N$, the runs spread widely; by $N = 5{,}000$, all runs cluster within R$ 200 of the analytical mean. The Chebyshev 95% band confirms the convergence rate.

### Experiment B: CLT Normality

The standardised mean of LogNormal salaries is visibly non-Normal at $n = 1$ but closely matches $N(0,1)$ by $n = 30$ (Figure 2). QQ-plots confirm: $R^2 > 0.999$ at $n = 100$.

### Experiment C: Full Budget Simulation

Running $N = 50{,}000$ iterations with default parameters:

![Budget Simulation](../figures/budget_simulation.png)
*Figure 4: Budget cost distribution (left: histogram, right: CDF) with mean, P5/P95, and budget ceiling annotated.*

The simulation recovers the analytical $E[X_{\text{total}}] \approx R\$ \, 11.55M$ within 0.1%. The distribution is right-skewed (driven by LogNormal salaries), with a 90% range spanning roughly R$ 1.6M.

### Experiment D: Variance Reduction

At $N = 5{,}000$, control variates reduce the 95% CI width by approximately 10× compared to naive MC (Figure 3). Antithetic variates provide a modest improvement. The control variate's power comes from the high correlation ($\rho \approx 0.99$) between total cost and raw salary sum.

### Experiment E: Sensitivity Analysis

Which parameters matter most? Varying each parameter by ±20%:

![Sensitivity Tornado](../figures/sensitivity_tornado.png)
*Figure 5: Tornado chart showing parameter impact on $E[X_{\text{total}}]$.*

The salary log-mean $\mu_s$ and headcount $n$ dominate. Benefits multiplier $\beta$ has proportional impact. Overtime and incident parameters have negligible effect on the expected total — consistent with their ~3% share of the budget.

**Practical implication:** improving the estimate of average salary matters far more than refining overtime or incident assumptions.

### Key Findings

| Metric | Value |
|--------|-------|
| Analytical $E[X_{\text{total}}]$ | R$ 11.55M |
| MC mean (N=50K) | Within 0.1% of analytical |
| 95% CI half-width (N=50K) | ~R$ 4K |
| P5–P95 range | ~R$ 1.6M |
| Most sensitive parameter | $\mu_s$ (salary log-mean) |
| Best variance reduction | Control variates (~10–50×) |

---

## 10. A Practical Framework for Budget Analysts

### When to Use Monte Carlo

- **Use MC** when the budget has stochastic components (variable headcount, uncertain overtime, unpredictable incidents) and you need to quantify risk.
- **A spreadsheet suffices** when all components are truly deterministic or when uncertainty is irrelevant to the decision.

### Recommended Workflow

1. **Define the model.** Identify which budget components are random and choose distributions based on historical data or expert judgement.
2. **Compute analytical moments.** Calculate $E[X]$ and $\text{Var}(X)$ for validation.
3. **Run a pilot simulation** ($N = 100$–$500$) to estimate $\sigma$ and determine the required $N$ for your desired precision.
4. **Run the full simulation** with the computed $N$. Use control variates if a good control variable exists.
5. **Report results** as a distribution: mean, CI, P(overbudget), and key percentiles.

### How to Present Results

Replace:

> "The IT headcount budget for next year is R$ 11.55M."

With:

> "We are 95% confident the IT headcount cost will fall between R$ 10.7M and R$ 12.4M, with a mean of R$ 11.55M. There is approximately a 7% probability of exceeding the R$ 12.5M ceiling. The primary driver of uncertainty is salary variance."

---

## 11. Conclusion

A point-estimate budget is a single sample from an unknown distribution. It carries no information about its own uncertainty.

This article built the mathematical machinery to replace that single number with a full probability distribution. Starting from the definition of random variables, we proved that averaging independent simulations converges to the true expected cost (Law of Large Numbers), quantified the convergence rate (Central Limit Theorem), formalised the Monte Carlo estimator and its properties, and applied variance reduction techniques to make the simulation efficient.

The experimental validation confirmed: Monte Carlo recovers the analytical expected value, the CLT gives calibrated confidence intervals, and control variates provide an order-of-magnitude improvement in precision.

The next time someone asks for a budget number, give them a distribution.

---

## References

1. Casella, G. & Berger, R. (2002). *Statistical Inference*. Duxbury.
2. Robert, C. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
3. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
4. Gelman, A. et al. (2013). *Bayesian Data Analysis*. CRC Press.

---

## How to Reproduce

```bash
git clone https://github.com/brunoramosmartins/monte-carlo-budget-article.git
cd monte-carlo-budget-article
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,notebook]"
python scripts/exp_budget_simulation.py
python scripts/exp_sensitivity.py
pytest tests/
```

All figures are generated with fixed seeds for exact reproducibility.
