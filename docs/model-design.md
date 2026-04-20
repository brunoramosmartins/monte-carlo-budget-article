# Budget Model Design

## Philosophy

The model is intentionally **generic and minimal** — few variables, clear
structure, easy to expand. It models the annual cost of an IT team as a sum
of stochastic components, serving as one concrete instantiation of a general
budget template. No proprietary data is used; all parameters are realistic
but synthetic.

## Variables

| Variable | Symbol | Distribution | Rationale |
|----------|--------|-------------|-----------|
| Base salary per employee | $S_i$ | LogNormal($\mu_s$, $\sigma_s$) | Salaries are right-skewed (few high earners) |
| Benefits multiplier | $\beta$ | Deterministic (e.g., 1.80) | Encargos as fixed % of salary (expandable to stochastic) |
| Headcount | $n$ | Deterministic (e.g., 50) | Fixed for base model (expandable to Poisson for hiring) |
| Overtime hours per employee/month | $H_i$ | Poisson($\lambda_h$) | Discrete, rare events (expandable) |
| Overtime hourly rate | $r_{ot}$ | Deterministic | Derived from salary (expandable) |
| Severe incidents per year | $I$ | Poisson($\lambda_I$) | Rare events causing extra overtime |
| Cost per incident | $C_I$ | LogNormal($\mu_I$, $\sigma_I$) | Variable severity |

## Total Annual Cost

$$
X = \underbrace{\sum_{i=1}^{n} S_i \cdot \beta \cdot 12}_{\text{Term 1: annual salary + benefits}} + \underbrace{\sum_{i=1}^{n} H_i \cdot r_{ot} \cdot 12}_{\text{Term 2: regular overtime}} + \underbrace{\sum_{j=1}^{I} C_{I_j}}_{\text{Term 3: incident costs}}
$$

Where:
- **Term 1:** Annual salary cost with benefits for all employees
- **Term 2:** Regular overtime cost across all employees and months
- **Term 3:** Cost of severe incidents (random count, random severity)

## Default Parameters

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Headcount | $n$ | 50 | employees |
| Salary log-mean | $\mu_s$ | 9.2 | log(BRL) |
| Salary log-std | $\sigma_s$ | 0.3 | log(BRL) |
| Benefits multiplier | $\beta$ | 1.80 | dimensionless |
| Overtime hours (monthly, per employee) | $\lambda_h$ | 5 | hours/month |
| Overtime hourly rate | $r_{ot}$ | 80 | BRL/hour |
| Incidents per year | $\lambda_I$ | 3 | incidents/year |
| Incident cost log-mean | $\mu_I$ | 10.5 | log(BRL) |
| Incident cost log-std | $\sigma_I$ | 0.5 | log(BRL) |

### Interpretation of Salary Parameters

With $\mu_s = 9.2$ and $\sigma_s = 0.3$:

$$
E[S_i] = e^{\mu_s + \sigma_s^2 / 2} = e^{9.2 + 0.045} = e^{9.245} \approx R\$ \, 10{,}362
$$

$$
\text{Var}(S_i) = (e^{\sigma_s^2} - 1) \cdot e^{2\mu_s + \sigma_s^2} = (e^{0.09} - 1) \cdot e^{18.49} \approx 10{,}117{,}947
$$

$$
\text{SD}(S_i) \approx R\$ \, 3{,}181
$$

This represents a monthly salary distribution centered around R$ 10,362 with
a standard deviation of about R$ 3,181 — realistic for a mixed-seniority IT team.

## Analytical Expected Value (for validation)

### Term 1: Salary + Benefits

$$
E[\text{Term 1}] = n \cdot E[S_i] \cdot \beta \cdot 12 = 50 \times 10{,}362 \times 1.80 \times 12 \approx R\$ \, 11{,}190{,}960
$$

### Term 2: Overtime

$$
E[\text{Term 2}] = n \cdot E[H_i] \cdot r_{ot} \cdot 12 = 50 \times 5 \times 80 \times 12 = R\$ \, 240{,}000
$$

### Term 3: Incidents

$$
E[\text{Term 3}] = E[I] \cdot E[C_I] = 3 \times e^{10.5 + 0.125} = 3 \times e^{10.625} \approx 3 \times 41{,}171 \approx R\$ \, 123{,}513
$$

### Total

$$
E[X_{\text{total}}] \approx 11{,}190{,}960 + 240{,}000 + 123{,}513 \approx R\$ \, 11{,}554{,}473
$$

**This value will be used to validate Monte Carlo simulation results in Phase 4.**

## Example Walkthrough

Consider a single simulation (one "possible year"):

1. Draw 50 salaries from LogNormal(9.2, 0.3): e.g., [R$ 8,500, R$ 12,100, ..., R$ 9,800]
2. Multiply each by benefits (1.80) and annualise (x12): salary cost per employee
3. Draw 50 overtime hours from Poisson(5) for each of 12 months
4. Multiply overtime hours by R$ 80/hour: overtime cost
5. Draw incident count from Poisson(3): e.g., I = 4
6. Draw 4 incident costs from LogNormal(10.5, 0.5): e.g., [R$ 35K, R$ 52K, R$ 28K, R$ 71K]
7. Sum all three terms: this is ONE sample of $X_{\text{total}}$

Repeat 10,000 times to get the distribution of $X_{\text{total}}$.

## Generalization

### The Template Structure

The IT headcount model above is one instantiation of a **general stochastic
budget template** with three structural components:

$$
X_{\text{total}} = \underbrace{\text{Proportional costs}}_{\text{scale with a count}} + \underbrace{\text{Fixed / periodic costs}}_{\text{deterministic or low-variance}} + \underbrace{\text{Compound rare events}}_{\text{random count} \times \text{random severity}}
$$

This decomposition applies to any budget where:

1. **Proportional costs** scale with some unit count (employees, servers,
   campaigns) and each unit carries its own distributional uncertainty.
2. **Fixed or periodic costs** are either deterministic or have low relative
   variance (e.g., licensing fees, rent).
3. **Rare disruptive events** occur at a random rate and carry variable cost
   per occurrence (compound Poisson structure).

### Other Budget Domains That Fit This Pattern

| Domain | Proportional | Fixed / Periodic | Compound Events |
|--------|-------------|-----------------|-----------------|
| **Cloud infrastructure** | Per-instance compute cost (varies with workload) | Reserved-instance commitments, license fees | Outage-driven autoscaling spikes |
| **Marketing** | Cost-per-lead times lead volume | Agency retainers, platform subscriptions | Viral campaign surges or PR crises |
| **Construction projects** | Material cost per unit area | Permits, insurance, site overhead | Weather delays, supply-chain disruptions |

### How to Instantiate the Template for a New Domain

1. **Identify the unit count** — the quantity that drives proportional costs
   (headcount, server count, campaign impressions, square metres). Decide
   whether it is deterministic or stochastic.
2. **Choose distributions for per-unit costs** — LogNormal is a good default
   for positive, right-skewed costs; Normal works for tightly controlled prices.
3. **Enumerate fixed charges** — list costs that do not scale with the unit
   count. These can start as deterministic and be promoted to random variables
   if uncertainty is material.
4. **Model rare events as compound Poisson** — pick a Poisson rate for event
   frequency and a distribution (e.g., LogNormal) for per-event severity.
5. **Calibrate parameters** — use historical data, expert judgement, or
   sensitivity analysis to set distribution parameters.
6. **Validate analytically** — derive $E[X]$ and $\text{Var}(X)$ from the
   chosen distributions and confirm that Monte Carlo results match.

The mathematical machinery (LLN, CLT, variance reduction) carries over
unchanged — only the parameter names and distributional choices differ.

## Expansion Points (documented, not implemented in v1)

### 1. Stochastic Headcount

$n \sim \text{Poisson}(\lambda_n)$ to model hiring uncertainty. The total
salary cost becomes a random sum of random variables (compound Poisson).

### 2. Stochastic Benefits Multiplier

$\beta \sim \text{Uniform}(1.75, 1.85)$ to model uncertainty in benefit
rates due to policy changes or negotiation outcomes.

### 3. Turnover Model

Employees leave at rate $p_{\text{leave}}$ and are replaced at potentially
different salary levels. This introduces serial dependence within the year.

### 4. Inflation Adjustment

Salary growth rate $g \sim \text{Normal}(\mu_g, \sigma_g)$ applied mid-year
for annual adjustments.

### 5. Correlation Between Salary and Overtime

High-seniority employees may have lower overtime rates but higher hourly
costs. Model via copula or conditional distributions.
