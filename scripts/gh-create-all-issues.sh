#!/usr/bin/env bash
# =============================================================================
# GitHub Issues — All Phases (Phase 1–9)
# Phase 0 issues are created by gh-setup-phase0.sh
# Run from WSL with: bash scripts/gh-create-all-issues.sh
# Requires: gh CLI authenticated, milestones already created
# =============================================================================

set -euo pipefail

REPO="brunoramosmartins/monte-carlo-budget-article"

echo "============================================"
echo "  Creating Issues — Phases 1 through 9"
echo "============================================"
echo ""

# =============================================================================
# PHASE 1 — Probability Foundations
# =============================================================================
echo "[Phase 1] Creating issues..."

# Issue #4
gh issue create \
  --repo "$REPO" \
  --title "[Phase 1] Derive expected value and variance from definitions" \
  --label "phase:1,type:theory,priority:critical" \
  --milestone "Phase 1 — Probability Foundations" \
  --body "$(cat <<'EOF'
## Context
Every Monte Carlo result depends on E[X] and Var(X). These must be derived
from scratch — not just stated — to build the mathematical foundation for
CLT and convergence proofs later.

## Tasks
- [ ] Define E[X] for continuous and discrete cases
- [ ] Prove linearity of expectation (from integral definition)
- [ ] Define Var(X) and prove the computational formula
- [ ] Prove Var(aX + b) = a²Var(X)
- [ ] Prove Var(X + Y) for independent and dependent cases
- [ ] Derive E and Var for LogNormal from Normal MGF
- [ ] Derive E and Var for Poisson from definition

## Definition of Done
- [ ] All proofs are step-by-step in `notes/phase1-probability.md`
- [ ] Each proof includes a concrete numerical example
- [ ] LogNormal and Poisson moments are derived, not just stated

## References
- Casella & Berger, Statistical Inference, Ch. 2
- Any probability textbook covering MGFs
EOF
)"
echo "  Created: [Phase 1] Derive expected value and variance from definitions"

# Issue #5
gh issue create \
  --repo "$REPO" \
  --title "[Phase 1] Compute analytical moments of the budget model" \
  --label "phase:1,type:theory,priority:high" \
  --milestone "Phase 1 — Probability Foundations" \
  --body "$(cat <<'EOF'
## Context
Before simulating, we need the analytical answer. This serves two purposes:
(1) validates the simulation later, and (2) shows what Monte Carlo adds
beyond the analytical mean (the full distribution shape).

## Tasks
- [ ] Express X_total = Σ S_i·β·12 + Σ H_i·r_ot·12 + Σ C_Ij
- [ ] Compute E[X_total] using linearity of expectation
- [ ] Compute Var(X_total) assuming independence between terms
- [ ] Plug in default parameters and get numerical values
- [ ] Document: "Monte Carlo will recover these moments AND give us the full distribution"

## Definition of Done
- [ ] E[X_total] and Var(X_total) computed symbolically and numerically
- [ ] All steps shown (no "it can be shown that...")
- [ ] Default parameter values produce a realistic budget range

## References
- Budget model spec from `docs/model-design.md`
EOF
)"
echo "  Created: [Phase 1] Compute analytical moments of the budget model"

echo ""

# =============================================================================
# PHASE 2 — Convergence Theorems
# =============================================================================
echo "[Phase 2] Creating issues..."

# Issue #6
gh issue create \
  --repo "$REPO" \
  --title "[Phase 2] Prove Markov, Chebyshev, and the Weak LLN" \
  --label "phase:2,type:theory,priority:critical" \
  --milestone "Phase 2 — Convergence Theorems" \
  --body "$(cat <<'EOF'
## Context
The Weak LLN is THE theorem that justifies Monte Carlo. Its proof chain is:
Markov → Chebyshev → WLLN. Each step must be derived explicitly.

## Tasks
- [ ] Prove Markov's inequality from the integral definition
- [ ] Prove Chebyshev as corollary of Markov on (X − μ)²
- [ ] Prove WLLN: P(|X̄_n − μ| ≥ ε) ≤ σ²/(nε²) → 0
- [ ] State SLLN with intuition and proof sketch
- [ ] Write interpretation paragraph connecting to Monte Carlo:
      "the sample mean of N simulated budgets converges to E[X_total]"

## Definition of Done
- [ ] Complete proof chain: Markov → Chebyshev → WLLN, no skipped steps
- [ ] Each inequality includes a worked numerical example
- [ ] Connection to Monte Carlo is explicit, not hand-wavy

## References
- Casella & Berger, Ch. 5
- Probability and Statistics for Engineering and the Sciences (Devore)
EOF
)"
echo "  Created: [Phase 2] Prove Markov, Chebyshev, and the Weak LLN"

# Issue #7
gh issue create \
  --repo "$REPO" \
  --title "[Phase 2] Implement LLN convergence visualization" \
  --label "phase:2,type:code,type:experiment,priority:high" \
  --milestone "Phase 2 — Convergence Theorems" \
  --body "$(cat <<'EOF'
## Context
The convergence plot is the article's first major figure: it shows the
sample mean of simulated costs stabilizing as N grows, with Chebyshev
bounds overlaid. This turns the abstract theorem into something visual.

## Tasks
- [ ] Generate N samples from LogNormal(9.2, 0.3) for N = 1 to 10,000
- [ ] Compute running mean: X̄_n for each n
- [ ] Compute Chebyshev bounds: μ ± σ/√n · (1/√α) for α = 0.05
- [ ] Plot: running mean with Chebyshev bounds and true E[X]
- [ ] Add multiple independent runs (5–10) to show variability
- [ ] Save to `figures/lln_convergence.png`
- [ ] Create notebook `notebooks/02_lln_convergence.ipynb`

## Definition of Done
- [ ] Figure clearly shows convergence with bounds
- [ ] Multiple runs show variability at small N, convergence at large N
- [ ] Notebook is self-contained and executable
- [ ] Author has run tests: `pytest tests/` (remind in chat)

## References
- Theory from Issue #6
EOF
)"
echo "  Created: [Phase 2] Implement LLN convergence visualization"

echo ""

# =============================================================================
# PHASE 3 — CLT & Confidence Intervals
# =============================================================================
echo "[Phase 3] Creating issues..."

# Issue #8
gh issue create \
  --repo "$REPO" \
  --title "[Phase 3] Prove the Central Limit Theorem (MGF approach)" \
  --label "phase:3,type:theory,priority:critical" \
  --milestone "Phase 3 — CLT & Confidence Intervals" \
  --body "$(cat <<'EOF'
## Context
The CLT is what turns Monte Carlo from "the mean converges" (LLN) into
"we can build confidence intervals around the mean." Without the CLT, we
know the estimator is right but not how right.

## Tasks
- [ ] Review MGF definition and uniqueness theorem
- [ ] Derive MGF of N(0,1): M(t) = e^{t²/2}
- [ ] State CLT: √n(X̄_n − μ)/σ →_d N(0,1)
- [ ] Proof:
      1. Define Z_i = (X_i − μ)/σ, so E[Z_i] = 0, Var(Z_i) = 1
      2. Sum: S_n = (Z_1 + ... + Z_n)/√n
      3. MGF: M_{S_n}(t) = [M_Z(t/√n)]^n
      4. Taylor: log M_Z(t/√n) = t²/(2n) + O(n^{-3/2})
      5. Limit: M_{S_n}(t) → e^{t²/2}
      6. Conclude by uniqueness
- [ ] State Berry-Esseen and interpret the O(1/√n) rate

## Definition of Done
- [ ] Complete proof with all Taylor expansion steps shown
- [ ] Each step has a marginal note explaining why it works
- [ ] Connection to Monte Carlo CI is made explicit at the end

## References
- Casella & Berger, Theorem 5.5.14
- Billingsley, Probability and Measure (for char. function version)
EOF
)"
echo "  Created: [Phase 3] Prove the Central Limit Theorem (MGF approach)"

# Issue #9
gh issue create \
  --repo "$REPO" \
  --title "[Phase 3] Derive CI formulas and implement CLT visualization" \
  --label "phase:3,type:theory,type:code,priority:high" \
  --milestone "Phase 3 — CLT & Confidence Intervals" \
  --body "$(cat <<'EOF'
## Context
Confidence intervals are the practical payoff of the CLT for this article.
A budget analyst needs to say "with 95% confidence, the budget is between
X and Y" — and this issue provides the mathematical justification.

## Tasks
- [ ] Derive CI formula from CLT: X̄ ± z·s/√N
- [ ] Derive required N for target precision: N ≥ (z·σ/ε)²
- [ ] Compute: for budget with σ = R$ 500K and ε = R$ 100K at 95%,
      N ≥ (1.96 · 500,000 / 100,000)² ≈ 97
- [ ] Implement CLT visualization:
      - Sum of n LogNormals, standardized, for n = 1, 5, 10, 30, 100
      - Histogram overlay with N(0,1) PDF
      - QQ-plot for n = 30 and n = 100
- [ ] Save figures

## Definition of Done
- [ ] CI formula derived step-by-step
- [ ] Required N formula derived and applied to budget example
- [ ] Figures show normality emerging clearly
- [ ] Author has run tests (remind in chat)

## References
- Theory from Issue #8
EOF
)"
echo "  Created: [Phase 3] Derive CI formulas and implement CLT visualization"

echo ""

# =============================================================================
# PHASE 4 — Monte Carlo Method
# =============================================================================
echo "[Phase 4] Creating issues..."

# Issue #10
gh issue create \
  --repo "$REPO" \
  --title "[Phase 4] Formalize MC estimator: unbiasedness, consistency, convergence rate" \
  --label "phase:4,type:theory,priority:critical" \
  --milestone "Phase 4 — Monte Carlo Method" \
  --body "$(cat <<'EOF'
## Context
The Monte Carlo estimator must be formally justified. This issue ties
together the LLN (convergence) and CLT (error quantification) from
previous phases into a single coherent framework applied to budget estimation.

## Tasks
- [ ] Define θ̂_N = (1/N) Σ g(X_i) as the Monte Carlo estimator
- [ ] Prove E[θ̂_N] = θ (unbiasedness)
- [ ] Prove θ̂_N → θ in probability (consistency via WLLN)
- [ ] Derive SE = σ/√N and explain the O(1/√N) rate
- [ ] Show: 10× more precision requires 100× more samples
- [ ] Contrast with deterministic quadrature: MC rate is dimension-free

## Definition of Done
- [ ] All three properties (unbiased, consistent, asymptotically normal) proved
- [ ] Convergence rate explained with practical implications
- [ ] Dimension-free advantage stated and contextualized

## References
- Robert & Casella, Monte Carlo Statistical Methods, Ch. 3
- Notes from Phase 2 (LLN) and Phase 3 (CLT)
EOF
)"
echo "  Created: [Phase 4] Formalize MC estimator"

# Issue #11
gh issue create \
  --repo "$REPO" \
  --title "[Phase 4] Implement budget model, MC engine, and analysis tools" \
  --label "phase:4,type:code,priority:critical" \
  --milestone "Phase 4 — Monte Carlo Method" \
  --body "$(cat <<'EOF'
## Context
This is the main implementation phase. The budget model, simulation engine,
and analysis tools are the code backbone of the article. They must be
modular, tested, and documented.

## Tasks
- [ ] Implement `src/model.py`:
      - `BudgetModel` class with configurable parameters
      - `simulate_one_year()` method returning total cost
      - Default parameters from `docs/model-design.md`
- [ ] Implement `src/monte_carlo.py`:
      - `MonteCarloSimulator` class
      - `run(n_iterations, seed)` → array of costs
      - Store raw results for later analysis
- [ ] Implement `src/analysis.py`:
      - `compute_ci(samples, alpha)` → (lower, upper)
      - `prob_over_budget(samples, budget)` → float
      - `summary_stats(samples)` → dict with mean, std, percentiles
- [ ] Create tests (DO NOT RUN — ask author):
      - `tests/test_model.py`: known parameters → expected mean within tolerance
      - `tests/test_monte_carlo.py`: reproducibility with fixed seed
      - `tests/test_analysis.py`: CI contains true mean in repeated trials

## Definition of Done
- [ ] All three modules implemented with type hints and docstrings
- [ ] Tests created in `tests/`
- [ ] Reminded author to run `pytest tests/` and `ruff check .`

## References
- Budget model spec from `docs/model-design.md`
- Analytical moments from Issue #5
EOF
)"
echo "  Created: [Phase 4] Implement budget model, MC engine, and analysis tools"

# Issue #12
gh issue create \
  --repo "$REPO" \
  --title "[Phase 4] First full budget simulation and validation" \
  --label "phase:4,type:experiment,priority:high" \
  --milestone "Phase 4 — Monte Carlo Method" \
  --body "$(cat <<'EOF'
## Context
The first end-to-end simulation validates that the code recovers the
analytical moments derived in Phase 1. This is the moment where theory
meets empirical verification.

## Tasks
- [ ] Run simulation: N=10,000, default parameters, seed=42
- [ ] Compare sample mean to analytical E[X_total] (should match within CI)
- [ ] Compare sample variance to analytical Var(X_total)
- [ ] Compute 95% CI and interpret
- [ ] Compute P(overbudget) for a hypothetical budget ceiling
- [ ] Plot histogram with mean, CI bounds, and budget ceiling annotated
- [ ] Create notebook `notebooks/04_monte_carlo_core.ipynb`

## Definition of Done
- [ ] Sample mean within 1% of analytical E[X_total]
- [ ] Histogram is publication-quality
- [ ] Notebook tells a complete story from model setup to interpretation

## References
- Analytical moments from Phase 1, Issue #5
- Code from Issue #11
EOF
)"
echo "  Created: [Phase 4] First full budget simulation and validation"

echo ""

# =============================================================================
# PHASE 5 — Variance Reduction
# =============================================================================
echo "[Phase 5] Creating issues..."

# Issue #13
gh issue create \
  --repo "$REPO" \
  --title "[Phase 5] Derive antithetic variates and control variates" \
  --label "phase:5,type:theory,priority:high" \
  --milestone "Phase 5 — Variance Reduction" \
  --body "$(cat <<'EOF'
## Context
Variance reduction is what separates a Monte Carlo tutorial from a serious
treatment. These techniques demonstrate mathematical depth and are directly
applicable to the budget problem.

## Tasks
- [ ] Derive antithetic variates:
      - Define the paired estimator
      - Prove variance formula with covariance term
      - Show when Cov < 0 (monotone g with inverse CDF trick)
- [ ] Derive control variates:
      - Define the controlled estimator with coefficient c
      - Derive optimal c* via calculus (minimize variance)
      - Prove variance reduction formula: Var(1 − ρ²)/N
      - Identify control variate for budget model: Σ S_i
- [ ] Derive stratified sampling:
      - Formal definition of strata and allocation
      - Prove Var_SS ≤ Var_MC (Jensen's inequality argument)

## Definition of Done
- [ ] All three techniques derived with complete proofs
- [ ] Each includes a concrete application to the budget model
- [ ] Optimal coefficient c* for control variates is derived, not just stated

## References
- Robert & Casella, Monte Carlo Statistical Methods, Ch. 4
- Glasserman, Monte Carlo Methods in Financial Engineering, Ch. 4
EOF
)"
echo "  Created: [Phase 5] Derive antithetic variates and control variates"

# Issue #14
gh issue create \
  --repo "$REPO" \
  --title "[Phase 5] Implement variance reduction and compare efficiency" \
  --label "phase:5,type:code,type:experiment,priority:high" \
  --milestone "Phase 5 — Variance Reduction" \
  --body "$(cat <<'EOF'
## Context
The implementation proves the theory works: antithetic and control variates
should produce tighter CIs than naive Monte Carlo for the same N.

## Tasks
- [ ] Implement `antithetic_mc()` in `src/variance_reduction.py`
- [ ] Implement `control_variate_mc()` with automatic c* estimation
- [ ] Implement `stratified_mc()` with configurable strata
- [ ] Create tests (DO NOT RUN):
      - Antithetic variance ≤ naive variance
      - Control variate variance ≤ naive variance
      - Results reproducible with fixed seed
- [ ] Run comparison: N=10,000, all methods, same budget model
- [ ] Create figure: CI width by method (bar chart or error band plot)
- [ ] Compute variance reduction ratios

## Definition of Done
- [ ] All three methods implemented and tested
- [ ] Comparison figure clearly shows variance reduction
- [ ] Reminded author to run `pytest tests/` and `ruff check .`

## References
- Theory from Issue #13
EOF
)"
echo "  Created: [Phase 5] Implement variance reduction and compare efficiency"

echo ""

# =============================================================================
# PHASE 6 — Bayesian Comparison
# =============================================================================
echo "[Phase 6] Creating issues..."

# Issue #15
gh issue create \
  --repo "$REPO" \
  --title "[Phase 6] Write Bayesian comparison section" \
  --label "phase:6,type:theory,type:writing,priority:medium" \
  --milestone "Phase 6 — Bayesian Comparison" \
  --body "$(cat <<'EOF'
## Context
A complete treatment of budget estimation should acknowledge Bayesian
methods. This section positions Monte Carlo within the broader statistical
landscape and shows the author's awareness of alternatives.

## Tasks
- [ ] Write conceptual Bayes overview (no implementation)
- [ ] Define prior, likelihood, posterior in budget context
- [ ] Create comparison table: Frequentist MC vs Bayesian
- [ ] Discuss when each is more appropriate
- [ ] Connect to FYF: informal Bayesian updating in practice
- [ ] Keep to 500–700 words

## Definition of Done
- [ ] Section is conceptual, no code
- [ ] Comparison table is clear and fair to both approaches
- [ ] FYF connection is made naturally

## References
- Gelman et al., Bayesian Data Analysis (conceptual overview only)
EOF
)"
echo "  Created: [Phase 6] Write Bayesian comparison section"

echo ""

# =============================================================================
# PHASE 7 — Experiments & Visualizations
# =============================================================================
echo "[Phase 7] Creating issues..."

# Issue #16
gh issue create \
  --repo "$REPO" \
  --title "[Phase 7] Full budget simulation with publication-quality figures" \
  --label "phase:7,type:experiment,priority:critical" \
  --milestone "Phase 7 — Experiments & Visualizations" \
  --body "$(cat <<'EOF'
## Context
This is the article's centrepiece experiment: a complete Monte Carlo
simulation of the IT budget with all components, producing the main
figure and key statistics.

## Tasks
- [ ] Run simulation: N=50,000, all budget components, seed=42
- [ ] Create dual figure: histogram + CDF
- [ ] Annotate: mean, median, P5/P95, budget ceiling, P(overbudget)
- [ ] Export publication-quality PNG (300 DPI, clean labels)
- [ ] Create summary statistics table for the article

## Definition of Done
- [ ] Figure is publication-quality (legible at article width)
- [ ] All annotations are correct and match simulation output
- [ ] Script runs end-to-end with `python scripts/exp_budget_simulation.py`

## References
- Budget model from Phase 4
- All theory from Phases 1–5
EOF
)"
echo "  Created: [Phase 7] Full budget simulation with publication-quality figures"

# Issue #17
gh issue create \
  --repo "$REPO" \
  --title "[Phase 7] Sensitivity analysis and tornado chart" \
  --label "phase:7,type:experiment,priority:high" \
  --milestone "Phase 7 — Experiments & Visualizations" \
  --body "$(cat <<'EOF'
## Context
A budget model is only useful if you know which parameters matter most.
The sensitivity analysis ranks parameters by their impact on the total cost,
guiding where to invest effort in getting better estimates.

## Tasks
- [ ] Define base case: all default parameters
- [ ] Vary each parameter ±20%: μ_s, σ_s, β, n, λ_h, r_ot, λ_I, μ_I
- [ ] For each variation: run MC (N=10,000), record E[X] and Var(X)
- [ ] Compute impact: ΔE[X] and ΔVar(X) as % change from base
- [ ] Create tornado chart: horizontal bars ranked by |ΔE[X]|
- [ ] Save to `figures/sensitivity_tornado.png`

## Definition of Done
- [ ] All parameters are varied and ranked
- [ ] Tornado chart is readable and correctly ordered
- [ ] Key insight documented: which parameters dominate?

## References
- Budget model spec from `docs/model-design.md`
EOF
)"
echo "  Created: [Phase 7] Sensitivity analysis and tornado chart"

# Issue #18
gh issue create \
  --repo "$REPO" \
  --title "[Phase 7] Generate animated convergence GIF for LinkedIn" \
  --label "phase:7,type:experiment,type:content,priority:medium" \
  --milestone "Phase 7 — Experiments & Visualizations" \
  --body "$(cat <<'EOF'
## Context
The GIF is the LinkedIn content piece: a histogram forming in real-time
as simulation iterations increase. It visually demonstrates the LLN and
makes the article shareable.

## Tasks
- [ ] Use matplotlib.animation to create animated histogram
- [ ] Frames at N = 100, 200, 500, 1K, 2K, 5K, 10K
- [ ] Each frame: histogram of costs so far + running mean line + CI band
- [ ] Title updates with current N
- [ ] Export as GIF (pillow writer), ~5 seconds loop
- [ ] Also export key frames as PNG for the article

## Definition of Done
- [ ] GIF loops smoothly and shows convergence clearly
- [ ] File size < 5 MB (suitable for LinkedIn)
- [ ] Key frames exported as separate PNGs

## References
- matplotlib.animation documentation
- LinkedIn post outline in roadmap
EOF
)"
echo "  Created: [Phase 7] Generate animated convergence GIF for LinkedIn"

echo ""

# =============================================================================
# PHASE 8 — Article Writing
# =============================================================================
echo "[Phase 8] Creating issues..."

# Issue #19
gh issue create \
  --repo "$REPO" \
  --title "[Phase 8] Write article sections 1-5" \
  --label "phase:8,type:writing,priority:high" \
  --milestone "Phase 8 — Article Writing" \
  --body "$(cat <<'EOF'
## Context
The first half builds the mathematical foundation: from the intuition that
budgets are uncertain to the formal tools (LLN, CLT) that quantify that
uncertainty. The narrative must be accessible but rigorous.

## Tasks
- [ ] Write sections 1–5 following outline
- [ ] Include all derivations adapted from theory notes
- [ ] Embed convergence and CLT figures
- [ ] Define all notation on first use (create a notation summary box)
- [ ] Ensure a reader with calculus background can follow every step

## Definition of Done
- [ ] Sections 1–5 complete in `article/monte-carlo-budget.md`
- [ ] All derivations are self-contained (no "see notes")
- [ ] Notation is consistent
- [ ] FYF is mentioned naturally in intro without proprietary details

## References
- `notes/phase1-probability.md`, `notes/phase2-convergence.md`, `notes/phase3-clt.md`
EOF
)"
echo "  Created: [Phase 8] Write article sections 1-5"

# Issue #20
gh issue create \
  --repo "$REPO" \
  --title "[Phase 8] Write article sections 6-11" \
  --label "phase:8,type:writing,priority:high" \
  --milestone "Phase 8 — Article Writing" \
  --body "$(cat <<'EOF'
## Context
The second half delivers the solution: Monte Carlo with variance reduction,
validates it experimentally, and provides actionable guidance. This is where
the article's value proposition is realized.

## Tasks
- [ ] Write sections 6–11 following outline
- [ ] Condense variance reduction proofs for article flow
- [ ] Present all experiments with figures and interpretation
- [ ] Create practical framework (flowchart or decision table)
- [ ] Write conclusion tying back to the opening hook
- [ ] Ensure the MD is ready for the author's HTML pipeline

## Definition of Done
- [ ] Sections 6–11 complete
- [ ] Article reads as a single cohesive narrative
- [ ] All figures are referenced and captioned
- [ ] Practical framework is actionable (not just theory)

## References
- All theory notes and experiment figures
EOF
)"
echo "  Created: [Phase 8] Write article sections 6-11"

echo ""

# =============================================================================
# PHASE 9 — Review & Publish
# =============================================================================
echo "[Phase 9] Creating issues..."

# Issue #21
gh issue create \
  --repo "$REPO" \
  --title "[Phase 9] Mathematical validation and code reproducibility" \
  --label "phase:9,type:review,priority:critical" \
  --milestone "Phase 9 — Review & Publish" \
  --body "$(cat <<'EOF'
## Context
A portfolio article with mathematical errors undermines credibility.
This issue is the final quality gate.

## Tasks
- [ ] Review all derivations in `article/monte-carlo-budget.md`
- [ ] Cross-check each numerical example against code
- [ ] Author runs full pipeline: install → scripts → tests → ruff
- [ ] Fix any discrepancies

## Definition of Done
- [ ] Zero mathematical errors
- [ ] All scripts produce identical figures with fixed seeds
- [ ] All tests pass, ruff is clean
- [ ] Author has personally verified (not Claude)

## References
- Full article
EOF
)"
echo "  Created: [Phase 9] Mathematical validation and code reproducibility"

# Issue #22
gh issue create \
  --repo "$REPO" \
  --title "[Phase 9] Publish to GitHub Pages and Medium" \
  --label "phase:9,type:infrastructure,type:writing,priority:high" \
  --milestone "Phase 9 — Review & Publish" \
  --body "$(cat <<'EOF'
## Context
The final step: making the article publicly accessible and shareable.

## Tasks
- [ ] Copy article MD to github.io repo
- [ ] Run MD → HTML pipeline
- [ ] Verify rendering (desktop + mobile)
- [ ] Publish Medium cross-post with canonical link
- [ ] Write LinkedIn post with GIF attachment
- [ ] Update README with live links and badges

## Definition of Done
- [ ] Article live on GitHub Pages
- [ ] Medium version published with canonical link
- [ ] LinkedIn post drafted with GIF
- [ ] README has all live links

## References
- Author's existing github.io repository and MD → HTML pipeline
EOF
)"
echo "  Created: [Phase 9] Publish to GitHub Pages and Medium"

echo ""
echo "============================================"
echo "  Done! Created 19 issues (Phases 1–9)"
echo ""
echo "  Summary:"
echo "  - Phase 1: 2 issues (#4, #5)"
echo "  - Phase 2: 2 issues (#6, #7)"
echo "  - Phase 3: 2 issues (#8, #9)"
echo "  - Phase 4: 3 issues (#10, #11, #12)"
echo "  - Phase 5: 2 issues (#13, #14)"
echo "  - Phase 6: 1 issue  (#15)"
echo "  - Phase 7: 3 issues (#16, #17, #18)"
echo "  - Phase 8: 2 issues (#19, #20)"
echo "  - Phase 9: 2 issues (#21, #22)"
echo "============================================"
