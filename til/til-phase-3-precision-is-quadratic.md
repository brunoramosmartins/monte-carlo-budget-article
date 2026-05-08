# TIL — Halving Your Confidence Interval Is Not Twice the Work, It Is Four Times

**Phase:** 3 · **Topic:** CLT, scaling law · **Domain:** Monte Carlo cost

## Hook

When stakeholders ask for "more precision", they often expect a linear
trade. Twice as tight an interval should cost twice as long, right?
The CLT says no. The scaling law is quadratic.

## Insight

The CI half-width from the CLT is

$$
\epsilon = z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{N}}
$$

To halve $\epsilon$, you need $\sqrt{N}$ to double — which means $N$ has
to **quadruple**. To divide by ten, $N$ has to multiply by 100. The price
of precision is paid in compute, and it is paid quadratically.

This is why variance reduction matters so much. A control variate that
multiplies effective $N$ by 50 is not "50× faster"; it is "the difference
between feasible and infeasible" once your tolerance moves from R$ 100K
to R$ 10K.

## Example

Pilot run gives $\sigma = R\$ 500K$. Required $N$ at 95% confidence:

| Half-width $\epsilon$ | Required $N$ |
|-----------------------|--------------|
| ±R$ 100K | 96 |
| ±R$ 50K | 384 |
| ±R$ 25K | 1,537 |
| ±R$ 10K | 9,604 |
| ±R$ 1K | 960,400 |

A CFO who casually asks "can you make the interval ten times tighter?"
just asked you for 100× more compute.

## Takeaway

State the precision *first*, then derive $N$. Working the other way around
("let's just run 10K") is how teams end up with confidence intervals that
sound impressive and decide nothing. The right number of simulations is
the smallest one that meets your tolerance — not the largest one your
laptop can take.
