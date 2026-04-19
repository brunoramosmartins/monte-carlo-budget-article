#!/usr/bin/env bash
# =============================================================================
# GitHub Setup Script — Phase 0
# Run from WSL with: bash scripts/gh-setup-phase0.sh
# Requires: gh CLI authenticated (gh auth status)
# =============================================================================

set -euo pipefail

REPO="brunoramosmartins/monte-carlo-budget-article"

echo "============================================"
echo "  GitHub Setup — Monte Carlo Budget Article"
echo "============================================"
echo ""

# -----------------------------------------------------------------------------
# 1. LABELS — Delete defaults, create project labels
# -----------------------------------------------------------------------------
echo "[1/3] Setting up labels..."

# Delete default GitHub labels that don't apply to this project
DEFAULT_LABELS=(
  "bug"
  "documentation"
  "duplicate"
  "enhancement"
  "good first issue"
  "help wanted"
  "invalid"
  "question"
  "wontfix"
)

echo "  Removing default labels..."
for label in "${DEFAULT_LABELS[@]}"; do
  gh label delete "$label" --repo "$REPO" --yes 2>/dev/null && \
    echo "    Deleted: $label" || \
    echo "    Skipped (not found): $label"
done

echo ""
echo "  Creating project labels..."

# Phase labels
gh label create "phase:0" --color "0E8A16" --description "Phase 0 — Foundation" --repo "$REPO" --force
gh label create "phase:1" --color "1D76DB" --description "Phase 1 — Probability Foundations" --repo "$REPO" --force
gh label create "phase:2" --color "5319E7" --description "Phase 2 — Convergence Theorems" --repo "$REPO" --force
gh label create "phase:3" --color "D93F0B" --description "Phase 3 — CLT & Confidence Intervals" --repo "$REPO" --force
gh label create "phase:4" --color "FBCA04" --description "Phase 4 — Monte Carlo Method" --repo "$REPO" --force
gh label create "phase:5" --color "B60205" --description "Phase 5 — Variance Reduction" --repo "$REPO" --force
gh label create "phase:6" --color "006B75" --description "Phase 6 — Bayesian Comparison" --repo "$REPO" --force
gh label create "phase:7" --color "1D76DB" --description "Phase 7 — Experiments & Visualizations" --repo "$REPO" --force
gh label create "phase:8" --color "0E8A16" --description "Phase 8 — Article Writing" --repo "$REPO" --force
gh label create "phase:9" --color "5319E7" --description "Phase 9 — Review & Publish" --repo "$REPO" --force

# Type labels
gh label create "type:theory" --color "C5DEF5" --description "Mathematical derivation or proof" --repo "$REPO" --force
gh label create "type:code" --color "BFD4F2" --description "Implementation task" --repo "$REPO" --force
gh label create "type:experiment" --color "D4C5F9" --description "Experimental validation or simulation" --repo "$REPO" --force
gh label create "type:writing" --color "FEF2C0" --description "Article writing task" --repo "$REPO" --force
gh label create "type:documentation" --color "0075CA" --description "Planning or project docs" --repo "$REPO" --force
gh label create "type:infrastructure" --color "E4E669" --description "Repo setup, CI, tooling" --repo "$REPO" --force
gh label create "type:review" --color "F9D0C4" --description "Review or validation task" --repo "$REPO" --force
gh label create "type:bug" --color "D73A4A" --description "Something is broken" --repo "$REPO" --force
gh label create "type:content" --color "BFDADC" --description "LinkedIn, Medium, or social content" --repo "$REPO" --force

# Priority labels
gh label create "priority:critical" --color "B60205" --description "Must be done, blocks other work" --repo "$REPO" --force
gh label create "priority:high" --color "D93F0B" --description "Important, do soon" --repo "$REPO" --force
gh label create "priority:medium" --color "FBCA04" --description "Can wait but should be done" --repo "$REPO" --force
gh label create "priority:low" --color "0E8A16" --description "Nice to have" --repo "$REPO" --force

echo "  Labels done."
echo ""

# -----------------------------------------------------------------------------
# 2. MILESTONES — One per phase
# -----------------------------------------------------------------------------
echo "[2/3] Creating milestones..."

gh api repos/"$REPO"/milestones -f title="Phase 0 — Foundation" -f state="open" -f description="Define thesis, scope, budget model, and repository skeleton."
gh api repos/"$REPO"/milestones -f title="Phase 1 — Probability Foundations" -f state="open" -f description="Formalize random variables, expected value, variance, key distributions."
gh api repos/"$REPO"/milestones -f title="Phase 2 — Convergence Theorems" -f state="open" -f description="Prove Markov, Chebyshev, Weak LLN. Implement convergence demonstration."
gh api repos/"$REPO"/milestones -f title="Phase 3 — CLT & Confidence Intervals" -f state="open" -f description="Prove CLT (MGF approach), derive confidence intervals for Monte Carlo."
gh api repos/"$REPO"/milestones -f title="Phase 4 — Monte Carlo Method" -f state="open" -f description="Formalize MC estimator, implement budget model and simulation engine."
gh api repos/"$REPO"/milestones -f title="Phase 5 — Variance Reduction" -f state="open" -f description="Derive and implement antithetic variates, control variates, stratified sampling."
gh api repos/"$REPO"/milestones -f title="Phase 6 — Bayesian Comparison" -f state="open" -f description="Brief conceptual comparison: frequentist MC vs Bayesian approach."
gh api repos/"$REPO"/milestones -f title="Phase 7 — Experiments & Visualizations" -f state="open" -f description="Run all experiments, create publication-quality figures and animated GIF."
gh api repos/"$REPO"/milestones -f title="Phase 8 — Article Writing" -f state="open" -f description="Assemble theory, experiments, and figures into the final article."
gh api repos/"$REPO"/milestones -f title="Phase 9 — Review & Publish" -f state="open" -f description="Final validation, publish to GitHub Pages, Medium, and LinkedIn."

echo "  Milestones done."
echo ""

# -----------------------------------------------------------------------------
# 3. ISSUES — Phase 0
# -----------------------------------------------------------------------------
echo "[3/3] Creating Phase 0 issues..."

# Get milestone number for Phase 0
MILESTONE_PHASE0=$(gh api repos/"$REPO"/milestones --jq '.[] | select(.title == "Phase 0 — Foundation") | .number')

# Issue #1 — Write thesis and define scope
gh issue create \
  --repo "$REPO" \
  --title "[Phase 0] Write thesis and define scope" \
  --label "phase:0,type:documentation,priority:high" \
  --milestone "Phase 0 — Foundation" \
  --body "$(cat <<'ISSUE_EOF'
## Context
The thesis anchors the entire article. Without a clear, falsifiable claim,
the article risks becoming a Monte Carlo tutorial instead of an argument for
why probabilistic budgeting is superior to point estimates.

## Tasks
- [ ] Draft central claim (v0.1)
- [ ] Define scope: probability theory, LLN, CLT, Monte Carlo, variance reduction,
      Bayesian comparison, applied IT budget model
- [ ] Define anti-scope: time-series, ARIMA, real company data, production deployment
- [ ] Identify target audience and prerequisite knowledge
- [ ] Write 1-paragraph abstract

## Definition of Done
- [ ] `docs/thesis.md` exists with thesis, scope, anti-scope, audience, abstract
- [ ] Thesis is a single falsifiable sentence
- [ ] Scope clearly separates theory phases from application phase

## References
- Project motivation (FYF context)
ISSUE_EOF
)"

echo "  Created: [Phase 0] Write thesis and define scope"

# Issue #2 — Design budget model and document expansion points
gh issue create \
  --repo "$REPO" \
  --title "[Phase 0] Design budget model and document expansion points" \
  --label "phase:0,type:documentation,priority:high" \
  --milestone "Phase 0 — Foundation" \
  --body "$(cat <<'ISSUE_EOF'
## Context
The budget model must be generic enough for a public article but realistic
enough to demonstrate Monte Carlo's value. It must start simple (few variables)
but document how each component could be expanded.

## Tasks
- [ ] Define all variables with distributions and rationale
- [ ] Write the total cost formula: X = salaries + overtime + incidents
- [ ] Choose default parameters (n=50, μ_s=9.2, σ_s=0.3, etc.)
- [ ] Compute analytical E[X] for the default parameters (for later validation)
- [ ] Document 5 expansion points with formulas but mark as "v2"
- [ ] Write a concrete example walkthrough

## Definition of Done
- [ ] `docs/model-design.md` exists with full spec
- [ ] Analytical E[X] is computed and documented
- [ ] Expansion points are clearly marked as future work
- [ ] A reader could implement the model from this document alone

## References
- Budget Model Design section of the roadmap
ISSUE_EOF
)"

echo "  Created: [Phase 0] Design budget model and document expansion points"

# Issue #3 — Configure repository, GitHub templates, and Claude Code rules
gh issue create \
  --repo "$REPO" \
  --title "[Phase 0] Configure repository, GitHub templates, and Claude Code rules" \
  --label "phase:0,type:infrastructure,priority:high" \
  --milestone "Phase 0 — Foundation" \
  --body "$(cat <<'ISSUE_EOF'
## Context
The repository must follow professional standards from day one. GitHub configuration
(labels, templates) ensures consistent issue tracking. Claude Code rules ensure
the AI assistant follows project conventions (no auto-commits, no auto-PRs,
no running tests).

## Tasks
- [ ] Initialize all directories with .gitkeep where needed
- [ ] Create `.claude/CLAUDE.md` with all project rules
- [ ] Create `.github/ISSUE_TEMPLATE/task.md` and `bug.md`
- [ ] Create `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Create `.github/labels.yml` for gh CLI label creation
- [ ] Write `pyproject.toml` with dependencies and ruff config (line-length=88, target=py310)
- [ ] Write initial `README.md` with project description and roadmap link
- [ ] Create `.gitignore`

## Definition of Done
- [ ] All directories exist
- [ ] `gh label create` can consume `labels.yml` (or script provided)
- [ ] Claude Code loads `.claude/CLAUDE.md` and follows rules
- [ ] `pip install -e ".[dev,notebook]"` succeeds
- [ ] `ruff check .` passes on empty project

## References
- Repository structure in the roadmap
- Claude Code configuration in the roadmap
ISSUE_EOF
)"

echo "  Created: [Phase 0] Configure repository, GitHub templates, and Claude Code rules"

echo ""
echo "============================================"
echo "  Setup complete!"
echo "  - Labels: 23 created"
echo "  - Milestones: 10 created"
echo "  - Issues: 3 created (Phase 0)"
echo "============================================"
