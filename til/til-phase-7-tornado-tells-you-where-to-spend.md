# TIL — A Sensitivity Tornado Is a Budget for Your Modelling Effort

**Phase:** 7 · **Topic:** Sensitivity analysis, decision-making · **Domain:** modelling priorities

## Hook

When you have a model with eight parameters, where do you spend the next
hour of your time? Tightening which estimate moves the answer? The
**tornado chart** is the cheapest way to answer that, and it is criminally
under-used in budget work.

## Insight

A sensitivity tornado runs the full simulation once per parameter, varying
that parameter by ±20% (or another defensible band) and holding the rest
fixed. For each parameter, record $\Delta E[X]$ and $\Delta P_{95}$.
Sort the bars by absolute impact. The result is a chart that reads top-to-
bottom: the parameters that move the answer the most are at the top.

The actionable insight is *not* "this parameter matters most". It is
**"this is where your next hour of effort should go"**. If you are
estimating the salary log-mean from 50 employees and the headcount from
HR records, and the salary log-mean has 10× the impact of headcount on
$E[X]$, then the question "should I spend two more days refining the
salary distribution or refining the headcount?" answers itself.

## Example

In our budget model:

| Parameter | $\Delta E[X]$ at ±20% |
|-----------|------------------------|
| $\mu_s$ (salary log-mean) | ±20% |
| $n$ (headcount) | ±20% |
| $\beta$ (benefits) | ±20% |
| $\sigma_s$ (salary log-std) | <1% |
| $\lambda_h$ (overtime rate) | <0.5% |
| $\lambda_I$ (incidents) | <0.5% |

The salary log-mean, headcount, and benefits multiplier together account
for >95% of the spread. Overtime and incidents are noise on the dial. A
team optimising the incident model is solving the wrong problem.

## Takeaway

Run the tornado *first*, before refining any parameter. It tells you
which knobs matter and which do not — saving you days of work modelling
the wrong thing. In any non-trivial model, the answer is concentrated in
2–3 parameters; the rest are decoration.
