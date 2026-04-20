# Article Outline — Why Your Budget Never Hits the Exact Number

## Target: 7,000-9,000 words

---

## Section 1 — Introduction (600 words)

**Source Phase:** —

**Hook:** "Your CFO asks for next year's budget. You open a spreadsheet,
multiply quantities by unit costs, add a contingency margin — and deliver a
number. A single number. But what if that number is just one sample from a
distribution you've never seen?"

**Content:**
- The periodic forecast review context: why organisations revisit budgets
  mid-cycle to detect deviations
- Why point estimates are the default and why they fail
- What this article offers: a mathematical framework for probabilistic budgeting
- Preview of the journey: probability -> convergence -> CLT -> Monte Carlo -> results

---

## Section 2 — The Point Estimate Problem (500 words)

**Source Phase:** Phase 1

**Content:**
- Formal definition: a point estimate is $\hat{\theta} = E[X]$
- What it discards: variance, skewness, tail risk
- Real-world consequence: "we budgeted R$ 12M but spent R$ 13.1M" — was this
  a failure or just a plausible outcome of the underlying uncertainty?
- Key insight: $E[X]$ tells you the center, but $F_X$ tells you the whole story

---

## Section 3 — Budget Components as Random Variables (600 words)

**Source Phase:** Phase 1

> **Note:** The framework is general — any budget with proportional costs, fixed
> charges, and rare events fits the same template. IT headcount is the case
> study used throughout this article.

**Content:**
- General template: proportional + fixed + compound rare events
- Case study instantiation: salaries (LogNormal), overtime (Poisson),
  incidents (compound Poisson)
- The budget model: $X = \sum S_i \cdot \beta \cdot 12 + \sum H_i \cdot r_{ot} \cdot 12 + \sum C_{I_j}$
- Expected value and variance derivations (condensed)
- Analytical E[X] for default parameters (for later validation)

---

## Section 4 — Will the Mean Converge? The Law of Large Numbers (700 words)

**Source Phase:** Phase 2

**Content:**
- Markov's inequality (brief)
- Chebyshev's inequality (with numerical example)
- Weak LLN: statement, proof (via Chebyshev), interpretation
- Strong LLN: statement, intuition
- What this means for Monte Carlo: "the sample mean of N simulated budgets
  converges to $E[X_{\text{total}}]$"
- Figure: LLN convergence plot (running mean stabilizing)

---

## Section 5 — How Wrong Can We Be? The Central Limit Theorem (800 words)

**Source Phase:** Phase 3

**Content:**
- MGF review (brief)
- CLT: statement, proof sketch (MGF approach, key Taylor expansion step)
- Berry-Esseen: how fast does normality kick in?
- From CLT to confidence intervals: $\bar{X} \pm z_{\alpha/2} \cdot s / \sqrt{N}$
- Choosing N: $N \geq (z \cdot \sigma / \epsilon)^2$
- Figure: CLT normality emergence (histogram + N(0,1) overlay)
- Figure: QQ-plot

---

## Section 6 — The Monte Carlo Estimator (700 words)

**Source Phase:** Phase 4

**Content:**
- Formal definition: $\hat{\mu}_N = (1/N) \sum g(X_i)$
- Unbiasedness proof (brief)
- Consistency: justified by LLN (Phase 4)
- Asymptotic normality: justified by CLT (Phase 5)
- Convergence rate: $O(1/\sqrt{N})$ — dimension-free advantage
- Implementation overview: the simulation loop
- Seed management for reproducibility

---

## Section 7 — Making It Faster: Variance Reduction (800 words)

**Source Phase:** Phase 5

**Content:**
- Why reduce variance? Tighter CIs for the same computational budget
- **Antithetic variates:** paired samples with negative correlation
  - Derivation of variance formula (condensed)
  - Application to budget model
- **Control variates:** leveraging known $E[\sum S_i]$
  - Optimal coefficient $c^*$ (derivation)
  - Variance reduction factor: $(1 - \rho^2)$
- **Stratified sampling:** partitioning by salary level
  - Proof: $\text{Var}_{SS} \leq \text{Var}_{MC}$ (brief)
- Figure: comparison of CI widths across methods

---

## Section 8 — A Bayesian Alternative (500 words)

**Source Phase:** Phase 6

**Content:**
- Conceptual overview: prior + likelihood -> posterior
- Budget context: prior = last year's distribution, likelihood = this year's data
- Connection to periodic forecast reviews: informal Bayesian updating in practice
- Comparison table: frequentist MC vs Bayesian
- When each approach is more appropriate
- Why this article chose frequentist: generality, no prior elicitation needed

---

## Section 9 — Experiments and Results (1,200 words)

**Source Phase:** Phase 7

**Content:**
- **Experiment A — LLN Convergence:** convergence plot with Chebyshev bounds
- **Experiment C — Full Simulation:** N=50,000, histogram + CDF, P(overbudget)
- **Experiment D — Variance Reduction:** CI width comparison across methods
- **Experiment E — Sensitivity Analysis:** tornado chart, which parameters matter
- Key findings summary:
  - Sample mean matches analytical E[X] within CI
  - Salary parameters dominate budget variance
  - Control variates provide ~X% variance reduction
  - 95% CI: [R$ A, R$ B]
  - P(overbudget at R$ 13M ceiling): ~Y%

---

## Section 10 — A Practical Framework for Budget Analysts (400 words)

**Source Phase:** —

**Content:**
- When to use Monte Carlo (and when a spreadsheet suffices)
- Choosing N: the trade-off between precision and computation
- Interpreting results for non-technical stakeholders
- Template: "We are X% confident the budget falls between A and B"
- Recommended workflow: define model -> run simulation -> report CI + P(overbudget)

---

## Section 11 — Conclusion (300 words)

**Source Phase:** —

**Content:**
- Restate thesis with evidence: point estimates discard uncertainty, MC recovers it
- Summary of mathematical journey: probability -> LLN -> CLT -> MC -> variance reduction
- What we gained: not just a number, but a distribution with quantified confidence
- Future directions: Bayesian updating with real data, time-series budget models
- Closing: "The next time someone asks for a budget number, give them a distribution."
