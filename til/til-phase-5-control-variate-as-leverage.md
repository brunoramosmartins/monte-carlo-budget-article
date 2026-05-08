# TIL — A Single Known Mean Can Replace 49,000 Simulations

**Phase:** 5 · **Topic:** Variance reduction, control variates · **Domain:** Monte Carlo efficiency

## Hook

The most surprising result in Monte Carlo is not that brute force works.
It is that brute force is wildly inefficient — and that one piece of
analytical knowledge can replace tens of thousands of simulations.

## Insight

A **control variate** is a function $h(X)$ whose expected value $E[h(X)]$
you know analytically, and which is correlated with the cost $g(X)$ you
are trying to estimate. The controlled estimator

$$
\hat{\theta}_{CV} = \hat{\theta}_N - c^* \left(\bar{h}_N - E[h(X)]\right)
$$

has variance

$$
\text{Var}(\hat{\theta}_{CV}) = \frac{\text{Var}(g(X))}{N} \cdot (1 - \rho^2)
$$

where $\rho$ is the correlation between $g$ and $h$. If $\rho = 0.99$,
the variance shrinks by a factor of $1 - 0.99^2 = 0.0199$ — about **50×**.

The trick is that $h$ is not a magic black box. It is the *dominant
component* of the cost. In a budget where salaries are 97% of the total,
$h(X) = \sum S_i$ is correlated with the total at $\rho \approx 0.99$ —
and its mean is just $n \cdot E[S_i]$, computable on a napkin.

## Example

For our 50-person budget, $N = 50{,}000$ naive simulations give the same
CI half-width as $N = 1{,}000$ control-variate simulations.

| Method | Runs to ±R$ 50K CI | Wall-clock | Cloud cost |
|--------|--------------------|------------|------------|
| Naive | 50,000 | ~30 s | ~50 vCPU-s |
| Control variate (salary sum) | 1,000 | ~0.6 s | ~1 vCPU-s |

The 49,000 simulations you did not run are the leverage you got from
*one analytical formula*.

## Takeaway

Find the dominant cost component, compute its expected value by hand, and
use it as a control variate. The combination of "one formula plus a small
simulation" beats "no formula plus a huge simulation" almost every time.
This is also the moment where mathematical intuition pays a visible
compute dividend — the kind of result that justifies the analyst's
modelling effort to the rest of the team.
