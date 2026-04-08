"""
tools/finance_tool.py
---------------------
Finance tools for EMI, interest, budgeting, and basic finance term explanations.
These tools return simple clean text so the agent can format the final answer nicely.
"""

import math
from langchain.tools import tool


@tool
def calculate_emi(principal: float, annual_rate: float, years: int) -> str:
    """
    Calculate the monthly EMI for a loan.

    Args:
        principal: Loan amount in INR.
        annual_rate: Annual interest rate in percentage.
        years: Loan tenure in years.
    """
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    if months <= 0:
        return "Invalid input: loan tenure must be greater than zero."

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * math.pow(1 + monthly_rate, months)
            / (math.pow(1 + monthly_rate, months) - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return (
        f"EMI calculation result: "
        f"principal=₹{principal:,.2f}, "
        f"annual_rate={annual_rate}%, "
        f"years={years}, "
        f"monthly_emi=₹{emi:,.2f}, "
        f"total_payment=₹{total_payment:,.2f}, "
        f"total_interest=₹{total_interest:,.2f}."
    )


@tool
def simple_interest(principal: float, rate: float, time: float) -> str:
    """
    Calculate simple interest and total amount.

    Args:
        principal: Principal amount in INR.
        rate: Annual interest rate in percentage.
        time: Time in years.
    """
    if time < 0:
        return "Invalid input: time cannot be negative."

    si = (principal * rate * time) / 100
    amount = principal + si

    return (
        f"Simple interest result: "
        f"principal=₹{principal:,.2f}, "
        f"rate={rate}%, "
        f"time={time} years, "
        f"simple_interest=₹{si:,.2f}, "
        f"total_amount=₹{amount:,.2f}."
    )


@tool
def compound_interest(principal: float, rate: float, time: float, n: int = 12) -> str:
    """
    Calculate compound interest and maturity amount.

    Args:
        principal: Principal amount in INR.
        rate: Annual interest rate in percentage.
        time: Time in years.
        n: Number of compounding periods per year.
    """
    if time < 0 or n <= 0:
        return "Invalid input: time must be non-negative and compounding frequency must be greater than zero."

    r = rate / 100
    amount = principal * math.pow((1 + r / n), n * time)
    ci = amount - principal

    freq_map = {
        1: "yearly",
        2: "half-yearly",
        4: "quarterly",
        12: "monthly",
        365: "daily",
    }
    freq_label = freq_map.get(n, f"{n} times per year")

    return (
        f"Compound interest result: "
        f"principal=₹{principal:,.2f}, "
        f"rate={rate}%, "
        f"time={time} years, "
        f"compounding={freq_label}, "
        f"compound_interest=₹{ci:,.2f}, "
        f"maturity_amount=₹{amount:,.2f}."
    )


@tool
def monthly_budget_split(salary: float) -> str:
    """
    Split salary using the 50/30/20 budgeting rule.

    Args:
        salary: Monthly salary in INR.
    """
    if salary < 0:
        return "Invalid input: salary cannot be negative."

    needs = salary * 0.50
    wants = salary * 0.30
    savings = salary * 0.20

    return (
        f"Monthly budget split result: "
        f"salary=₹{salary:,.2f}, "
        f"needs_50=₹{needs:,.2f}, "
        f"wants_30=₹{wants:,.2f}, "
        f"savings_20=₹{savings:,.2f}."
    )


@tool
def explain_finance_term(term: str) -> str:
    """
    Explain common basic finance terms in simple language.

    Example inputs:
    leverage, emi, simple interest, compound interest, principal, budget, loan
    """
    term_clean = term.strip().lower()

    finance_terms = {
        "leverage": (
            "Leverage means using borrowed money or fixed-cost funds to increase the potential return "
            "of an investment or business. It can increase profit, but it also increases risk."
        ),
        "emi": (
            "EMI stands for Equated Monthly Instalment. It is the fixed amount you pay every month "
            "to repay a loan, including both principal and interest."
        ),
        "simple interest": (
            "Simple interest is interest calculated only on the original principal amount for the full period."
        ),
        "compound interest": (
            "Compound interest is interest calculated on the principal and also on previously earned interest, "
            "so it grows faster than simple interest."
        ),
        "principal": (
            "Principal is the original amount of money borrowed, invested, or deposited."
        ),
        "interest rate": (
            "Interest rate is the percentage charged or earned on the principal amount over a period of time."
        ),
        "budget": (
            "A budget is a financial plan that shows how income will be divided among expenses, savings, and goals."
        ),
        "loan": (
            "A loan is money borrowed from a lender that must be repaid, usually with interest."
        ),
        "debt": (
            "Debt is money that a person or business owes to another person, bank, or institution."
        ),
        "savings": (
            "Savings is the portion of income that is set aside for future use instead of being spent immediately."
        ),
    }

    if term_clean in finance_terms:
        return f"Finance term explanation: term={term_clean}. meaning={finance_terms[term_clean]}"

    return (
        f"Finance term explanation: term={term_clean}. "
        f"meaning=Sorry, I do not have a stored explanation for this term yet."
    )