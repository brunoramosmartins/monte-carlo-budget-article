# TIL — Every Forecast Review You Have Ever Run Was Already Bayesian

**Phase:** 6 · **Topic:** Bayesian inference, forecast revision · **Domain:** budget lifecycle

## Hook

Most finance teams treat the periodic forecast review (FYF, rolling
forecast, monthly close-and-revise) as an act of judgement. Bayesian
inference is treated as a separate, exotic methodology. They are the
same thing — done with different rigour.

## Insight

A forecast review takes a prior belief (last month's expected outcome),
mixes it with new evidence (this month's actual spending), and produces
an updated belief (next month's expected outcome). That is *exactly*
Bayes' rule:

$$
P(\theta \mid \text{data}) \propto P(\text{data} \mid \theta) \cdot P(\theta)
$$

The difference between an informal forecast revision and a formal Bayesian
update is not the *direction* of reasoning — both go from prior to
posterior. The difference is whether the update is **auditable**: whether
you can reconstruct, six months later, why the forecast moved the way it
did, and whether the variance of your forecast shrank coherently with the
evidence.

When the prior comes from a Monte Carlo simulation (the *first version*
of the budget) and the likelihood is a parametric model of monthly
spending, the update is a one-line formula. The team gets a living
forecast that improves with every close, and a paper trail of how each
revision was justified.

## Example

Take a Normal-Normal conjugate update. Prior: $\theta \sim N(\mu_0, \tau_0^2)$.
Three months of data $x_1, x_2, x_3$ with known sampling variance $\sigma^2$.
Posterior:

$$
\theta \mid x_{1:3} \sim N\!\left(\frac{\tau_0^{-2} \mu_0 + 3\sigma^{-2} \bar{x}}{\tau_0^{-2} + 3\sigma^{-2}}, \; \frac{1}{\tau_0^{-2} + 3\sigma^{-2}}\right)
$$

The posterior mean is a precision-weighted average of prior and data.
Three months of clean data tighten the CI by roughly $\sqrt{3} \approx 1.7×$.
By month 12, the posterior has collapsed onto the realised cost.

## Takeaway

If your team already does forecast reviews, you already have a Bayesian
process — it is just unwritten. Writing it down (priors, likelihoods,
update rules) does not change *what* the team does. It changes whether
the result can be audited, communicated, and inherited by the next
analyst. That is the gap between a script and a data product.
