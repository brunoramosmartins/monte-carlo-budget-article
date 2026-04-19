"""Budget cost model for Monte Carlo simulation.

This module defines the stochastic budget model for IT headcount planning.
The model computes the total annual cost as the sum of three components:
salaries with benefits, regular overtime, and incident-driven costs.

All distributional choices and default parameters follow the specification
in ``docs/model-design.md``.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class BudgetModelParams:
    """Parameters for the IT headcount budget model.

    Parameters
    ----------
    n_employees : int
        Number of employees (deterministic headcount).
    mu_salary : float
        Log-mean of the monthly salary distribution (LogNormal parameter).
    sigma_salary : float
        Log-standard-deviation of the monthly salary distribution.
    benefits_multiplier : float
        Multiplicative factor for benefits (encargos) on top of salary.
    lambda_overtime : float
        Expected overtime hours per employee per month (Poisson rate).
    overtime_hourly_rate : float
        Cost per overtime hour in BRL.
    lambda_incidents : float
        Expected number of severe incidents per year (Poisson rate).
    mu_incident_cost : float
        Log-mean of per-incident cost (LogNormal parameter).
    sigma_incident_cost : float
        Log-standard-deviation of per-incident cost.
    """

    n_employees: int = 50
    mu_salary: float = 9.2
    sigma_salary: float = 0.3
    benefits_multiplier: float = 1.80
    lambda_overtime: float = 5.0
    overtime_hourly_rate: float = 80.0
    lambda_incidents: float = 3.0
    mu_incident_cost: float = 10.5
    sigma_incident_cost: float = 0.5


@dataclass
class YearResult:
    """Result of simulating one year of the budget model.

    Attributes
    ----------
    salary_cost : float
        Total annual salary cost including benefits (Term 1).
    overtime_cost : float
        Total annual overtime cost (Term 2).
    incident_cost : float
        Total cost of severe incidents (Term 3).
    total_cost : float
        Sum of all three terms.
    n_incidents : int
        Number of incidents that occurred.
    """

    salary_cost: float
    overtime_cost: float
    incident_cost: float
    total_cost: float
    n_incidents: int


class BudgetModel:
    """Stochastic budget model for IT headcount planning.

    The total annual cost is:

    .. math::
        X = \\sum_{i=1}^{n} S_i \\cdot \\beta \\cdot 12
            + \\sum_{i=1}^{n} H_i \\cdot r_{ot} \\cdot 12
            + \\sum_{j=1}^{I} C_j

    Parameters
    ----------
    params : BudgetModelParams
        Model parameters. Uses defaults from ``docs/model-design.md``
        if not provided.

    Examples
    --------
    >>> model = BudgetModel()
    >>> rng = np.random.default_rng(42)
    >>> result = model.simulate_one_year(rng)
    >>> isinstance(result.total_cost, float)
    True
    """

    def __init__(self, params: BudgetModelParams | None = None) -> None:
        self.params = params or BudgetModelParams()

    def simulate_one_year(self, rng: np.random.Generator) -> YearResult:
        """Simulate one fiscal year and return the cost breakdown.

        Parameters
        ----------
        rng : np.random.Generator
            Random number generator for reproducibility.

        Returns
        -------
        YearResult
            Breakdown of costs by component and total.
        """
        p = self.params

        # Term 1: salaries with benefits
        salaries = rng.lognormal(
            mean=p.mu_salary, sigma=p.sigma_salary, size=p.n_employees
        )
        salary_cost = float(np.sum(salaries) * p.benefits_multiplier * 12)

        # Term 2: overtime (per employee per month, summed over the year)
        overtime_hours = rng.poisson(
            lam=p.lambda_overtime, size=(p.n_employees, 12)
        )
        overtime_cost = float(np.sum(overtime_hours) * p.overtime_hourly_rate)

        # Term 3: incidents (compound Poisson)
        n_incidents = int(rng.poisson(lam=p.lambda_incidents))
        if n_incidents > 0:
            incident_costs = rng.lognormal(
                mean=p.mu_incident_cost,
                sigma=p.sigma_incident_cost,
                size=n_incidents,
            )
            incident_cost = float(np.sum(incident_costs))
        else:
            incident_cost = 0.0

        total_cost = salary_cost + overtime_cost + incident_cost

        return YearResult(
            salary_cost=salary_cost,
            overtime_cost=overtime_cost,
            incident_cost=incident_cost,
            total_cost=total_cost,
            n_incidents=n_incidents,
        )

    def analytical_expected_total(self) -> float:
        """Compute the analytical E[X_total] for validation.

        Returns
        -------
        float
            Expected total annual cost derived from distributional parameters.

        Notes
        -----
        Uses linearity of expectation and Wald's equation:

        .. math::
            E[X] = n \\cdot \\beta \\cdot 12 \\cdot E[S]
                   + n \\cdot r_{ot} \\cdot 12 \\cdot \\lambda_h
                   + \\lambda_I \\cdot E[C]
        """
        p = self.params
        e_salary = np.exp(p.mu_salary + p.sigma_salary**2 / 2)
        e_t1 = p.n_employees * p.benefits_multiplier * 12 * e_salary
        e_t2 = p.n_employees * p.overtime_hourly_rate * 12 * p.lambda_overtime
        e_incident = np.exp(p.mu_incident_cost + p.sigma_incident_cost**2 / 2)
        e_t3 = p.lambda_incidents * e_incident
        return e_t1 + e_t2 + e_t3

    def analytical_variance_total(self) -> float:
        """Compute the analytical Var(X_total) for validation.

        Returns
        -------
        float
            Variance of total annual cost assuming independence between terms.
        """
        p = self.params

        # Term 1 variance
        var_s = (np.exp(p.sigma_salary**2) - 1) * np.exp(
            2 * p.mu_salary + p.sigma_salary**2
        )
        var_t1 = p.n_employees * (p.benefits_multiplier * 12) ** 2 * var_s

        # Term 2 variance
        var_t2 = (
            p.n_employees
            * (p.overtime_hourly_rate * 12) ** 2
            * p.lambda_overtime
        )

        # Term 3 variance (compound Poisson)
        e_c2 = np.exp(
            2 * p.mu_incident_cost + 2 * p.sigma_incident_cost**2
        )
        var_t3 = p.lambda_incidents * e_c2

        return var_t1 + var_t2 + var_t3
