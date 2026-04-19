# Phase 6 — A Bayesian Alternative

## Overview

The Monte Carlo approach developed in Phases 1–5 is **frequentist**: we
assume a fixed model, simulate from it, and build confidence intervals.
This section briefly introduces the **Bayesian** perspective — not to
replace the frequentist framework, but to position it within the broader
statistical landscape and show awareness of alternatives.

No implementation is required. This is a conceptual section targeting
500–700 words in the final article.

---

## 1. Bayes' Theorem Applied to Budgets

In the Bayesian framework, unknown parameters are treated as random
variables with their own distributions. Bayes' theorem provides the
mechanism for updating beliefs as data arrives:

$$
P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \cdot P(\theta)
$$

| Component | Symbol | Budget Interpretation |
|-----------|--------|----------------------|
| **Prior** | $P(\theta)$ | What we believed about costs before the year started — e.g., last year's budget distribution, historical patterns, expert judgement |
| **Likelihood** | $P(\text{data} \mid \theta)$ | How well a specific cost parameter $\theta$ explains the spending data observed so far this year |
| **Posterior** | $P(\theta \mid \text{data})$ | Our updated belief about costs given what we have observed — this is the revised forecast |

### Example

Suppose we model the average monthly salary cost as $\theta$ with a prior
$\theta \sim N(\mu_0, \tau_0^2)$ based on last year's data. After observing
$m$ months of actual spending $(x_1, \ldots, x_m)$ with known variance
$\sigma^2$, the posterior is:

$$
\theta \mid x_1, \ldots, x_m \sim N\left(\frac{\tau_0^{-2} \mu_0 + m\sigma^{-2}\bar{x}}{\tau_0^{-2} + m\sigma^{-2}}, \; \frac{1}{\tau_0^{-2} + m\sigma^{-2}}\right)
$$

The posterior mean is a **precision-weighted average** of the prior mean
and the data mean. As more data arrives ($m$ grows), the posterior shifts
toward the data and the posterior variance shrinks.

---

## 2. Connection to FYF

The Forecast Year-end Financial (FYF) process is, in practice, **informal
Bayesian updating**:

1. **January:** The team starts with the approved budget (the prior).
2. **Each FYF review:** Actual spending data arrives (the likelihood).
   The forecast is revised — the posterior becomes the new prior for the
   next review.
3. **Year-end:** The final forecast reflects all accumulated data.

The difference is that FYF typically updates via spreadsheet adjustments
rather than formal probability distributions. A Bayesian model would make
the uncertainty explicit at every revision — not just the point estimate,
but the full posterior distribution.

---

## 3. Frequentist MC vs Bayesian: Comparison

| Aspect | Frequentist Monte Carlo | Bayesian |
|--------|------------------------|----------|
| **Parameters** | Fixed but unknown constants | Random variables with distributions |
| **Prior information** | Not used (or implicit in model choice) | Explicitly encoded as a prior $P(\theta)$ |
| **Data role** | Not used (simulated from assumed model) | Updates the prior via likelihood |
| **Output** | Confidence interval: "in 95% of repeated experiments, the CI contains $\theta$" | Credible interval: "there is a 95% probability that $\theta$ lies in this interval" |
| **Interpretation** | Frequentist: refers to long-run repeated sampling | Bayesian: probability statement about the parameter itself |
| **Computational method** | Forward simulation from the model | MCMC, variational inference, or conjugate updates |
| **Model specification** | Define distributions and parameters | Define distributions, parameters, AND priors |
| **Mid-year updating** | Requires re-specifying the model | Natural: posterior from month $m$ becomes prior for month $m+1$ |
| **Strengths** | No prior elicitation needed; simple to implement; results are objective | Incorporates prior knowledge; natural sequential updating; direct probability statements |
| **Weaknesses** | Cannot incorporate historical data formally; CI interpretation is subtle | Requires prior specification; computationally heavier; prior sensitivity |

---

## 4. When Each Approach Is More Appropriate

### Use Frequentist Monte Carlo When:

- **No historical data** is available (new team, new cost structure)
- The model structure is well-understood but parameter uncertainty is the
  concern
- Simplicity and transparency are priorities (e.g., presenting to non-technical
  stakeholders)
- The goal is to explore "what-if" scenarios under different assumptions

### Use Bayesian Methods When:

- **Historical data** from previous years is available and informative
- Sequential updating is needed (e.g., monthly FYF revisions)
- The analyst wants to make **direct probability statements** about parameters
  ("there is a 90% probability that the average salary cost is between X and Y")
- Multiple sources of information (expert judgement + data) need to be
  formally combined

### Why This Article Chose Frequentist MC

1. **Generality:** The frequentist approach works even without historical
   data — only a model specification is needed.
2. **No prior elicitation:** Choosing a prior distribution requires expertise
   and can be controversial. The frequentist approach avoids this debate.
3. **Pedagogical clarity:** The mathematical chain (LLN → CLT → CI) is
   self-contained and builds naturally from first principles.
4. **Practical simplicity:** A budget analyst can implement Monte Carlo in
   a spreadsheet or a short Python script without specialised Bayesian
   software.

The Bayesian approach is a natural extension for teams with historical
budget data — and it is worth noting that the Monte Carlo samples generated
by our frequentist engine could serve as the foundation for a Bayesian
model if priors were added later.
