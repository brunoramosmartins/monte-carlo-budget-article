# TIL — Monte Carlo Does Not Care How Big Your Input Vector Is

**Phase:** 4 · **Topic:** MC estimator, convergence rate · **Domain:** numerical methods

## Hook

If you have ever tried to integrate a function in 10 dimensions with a
trapezoidal rule, you know about the curse of dimensionality. Required
points scale as $N^d$ — exponential in dimension. By $d = 6$ you are
already done; by $d = 20$ you have given up. Monte Carlo does not have
this problem.

## Insight

The Monte Carlo standard error is

$$
\text{SE} = \frac{\sigma_g}{\sqrt{N}}
$$

Notice what is not in there: the dimension of $X$. Whether $X$ is a
scalar, a vector of 50 salaries, or a 600-dimensional matrix of
employees-by-months overtime hours, the convergence rate is identical:
$O(1/\sqrt{N})$.

That is because Monte Carlo does not visit a grid. It samples *paths
through the joint distribution*, one at a time. Each sample is one
"possible year" — fully high-dimensional, but you only need its scalar
output (the cost). The rate depends on the variance of that scalar, not
on the size of the input.

## Example

In our budget model, one simulation samples:

- 50 salaries (LogNormal)
- 50 × 12 = 600 overtime values (Poisson)
- 1 incident count (Poisson)
- Up to ~10 incident costs (LogNormal)

That is roughly **661 random numbers** per simulation. A 1,000-iteration
run draws ~661,000 random numbers and produces a CI as tight as a 1D
problem with the same variance would. No grid, no exponential blowup.

## Takeaway

When the input is high-dimensional, *use Monte Carlo*. Deterministic
quadrature dies on contact with dimension; MC barely notices it. This is
the property that makes simulation the only viable method for realistic
financial, physical, or operational models.
