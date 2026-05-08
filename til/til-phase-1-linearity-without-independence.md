# TIL — The Most Useful Theorem in Probability Has No Independence Hypothesis

**Phase:** 1 · **Topic:** Expected value, linearity · **Domain:** budget modelling

## Hook

Most introductions to probability lean hard on the independence assumption.
"If $X$ and $Y$ are independent…" is the qualifier that prefaces nearly
every formula in a textbook chapter. Linearity of expectation is the
exception — and it is the most useful theorem of the lot.

## Insight

For any random variables $X_1, \ldots, X_n$ — independent, dependent, or
correlated in ways nobody has measured — the expected value of the sum is
the sum of the expected values:

$$
E\left[\sum_{i=1}^n X_i\right] = \sum_{i=1}^n E[X_i]
$$

No independence required. No joint distribution required. No "assume
i.i.d." required.

For a budget model, this is liberating: the *expected* total cost is just
the sum of expected component costs, even if those components covary in
nasty ways. Variance is a different story (it has cross-covariance terms),
but the mean is bullet-proof.

## Example

Take a 50-person team. Salaries $S_i$ are LogNormal with $E[S_i] \approx
R\$ 10{,}362$. Whether or not senior people negotiate raises in clusters
(positive correlation) or compete for a fixed bonus pool (negative
correlation), the expected total salary is identically:

$$
E\left[\sum_{i=1}^{50} S_i\right] = 50 \times 10{,}362 = R\$ \, 518{,}100
$$

The correlation pattern affects how *spread out* the total is. It does not
affect the mean.

## Takeaway

When estimating a budget mean, you can ignore correlations. When estimating
its variance — or its CI — you cannot. The two questions are not the same,
and confusing them is one of the quiet ways a probabilistic budget gets
wrong.
