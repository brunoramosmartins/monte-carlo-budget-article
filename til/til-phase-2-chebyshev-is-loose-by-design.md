# TIL — Chebyshev's Inequality Is Loose, and That Is the Whole Point

**Phase:** 2 · **Topic:** Chebyshev, LLN · **Domain:** Monte Carlo bounds

## Hook

Anyone who applies Chebyshev's inequality to a real problem has the same
reaction: "the bound is *terrible*." For a Normal distribution,
$P(|X - \mu| \geq 2\sigma)$ is about 5%. Chebyshev guarantees only 25%.
Five times worse. So why use it?

## Insight

Chebyshev is loose **because it makes no distributional assumption**. The
bound $P(|X - \mu| \geq k\sigma) \leq 1/k^2$ holds for *any* random variable
with finite variance — Normal, LogNormal, Pareto, the bizarre output of
some custom budget model. You pay for that universality with a wide bound.

When you know the distribution is approximately Normal (e.g., via the CLT
on a sample mean), the CLT gives you something tighter. Chebyshev is the
fallback when you cannot make that assumption — and the *first thing* you
prove on your way to the LLN, because the LLN inherits Chebyshev's "no
distributional assumption" robustness.

## Example

For the salary mean of a 1,000-employee sample with $\sigma \approx R\$ 3{,}181$:

| Bound | $P(|\bar{X} - \mu| \geq R\$ 200)$ |
|-------|-----------------------------------|
| Chebyshev | $\leq \frac{(3181)^2}{1000 \times 200^2} \approx 25\%$ |
| CLT-based (95% CI) | $\approx 4\%$ |

Six-fold difference. The CLT wins on tightness. Chebyshev wins on robustness.

## Takeaway

A "loose" bound is not always a worse bound. It is a different *kind* of
guarantee — one that holds when you are unsure of the model. In risk work,
that universality is sometimes worth more than tightness. Use Chebyshev
when the distribution is suspect; use the CLT when it is trustworthy.
