"""UK take-home pay calculator.

Covers England, Wales and Northern Ireland for the 2026/27 tax year.
All figures are estimates. Check GOV.UK for official rates.
"""

# Income tax
PERSONAL_ALLOWANCE = 12_570
TAPER_THRESHOLD = 100_000  # allowance shrinks by £1 for every £2 earned above this
BASIC_RATE_BAND = 37_700
ADDITIONAL_RATE_THRESHOLD = 125_140
BASIC_RATE = 0.20
HIGHER_RATE = 0.40
ADDITIONAL_RATE = 0.45

# Employee National Insurance (Class 1)
NI_PRIMARY_THRESHOLD = 12_570
NI_UPPER_EARNINGS_LIMIT = 50_270
NI_MAIN_RATE = 0.08
NI_UPPER_RATE = 0.02

# Student loans: plan -> (yearly threshold, repayment rate)
STUDENT_LOAN_PLANS = {
    "none": (None, 0.0),
    "plan_2": (29_385, 0.09),
    "plan_5": (25_000, 0.09),
}


def personal_allowance(salary):
    """Tax-free allowance, reduced for salaries over £100,000."""
    if salary <= TAPER_THRESHOLD:
        return PERSONAL_ALLOWANCE
    reduction = (salary - TAPER_THRESHOLD) / 2
    return max(0, PERSONAL_ALLOWANCE - reduction)


def income_tax(salary):
    """Yearly income tax on a salary."""
    taxable = max(0, salary - personal_allowance(salary))
    tax = min(taxable, BASIC_RATE_BAND) * BASIC_RATE
    if taxable > BASIC_RATE_BAND:
        tax += (min(taxable, ADDITIONAL_RATE_THRESHOLD) - BASIC_RATE_BAND) * HIGHER_RATE
    if taxable > ADDITIONAL_RATE_THRESHOLD:
        tax += (taxable - ADDITIONAL_RATE_THRESHOLD) * ADDITIONAL_RATE
    return round(tax, 2)


def national_insurance(salary):
    """Yearly employee National Insurance."""
    ni = max(0, min(salary, NI_UPPER_EARNINGS_LIMIT) - NI_PRIMARY_THRESHOLD) * NI_MAIN_RATE
    if salary > NI_UPPER_EARNINGS_LIMIT:
        ni += (salary - NI_UPPER_EARNINGS_LIMIT) * NI_UPPER_RATE
    return round(ni, 2)


def student_loan(salary, plan="none"):
    """Yearly student loan repayment for the given plan."""
    if plan not in STUDENT_LOAN_PLANS:
        raise ValueError(f"Unknown student loan plan: {plan}")
    threshold, rate = STUDENT_LOAN_PLANS[plan]
    if threshold is None:
        return 0.0
    return round(max(0, salary - threshold) * rate, 2)


def take_home(salary, pension_percent=0, plan="none"):
    """Full breakdown of yearly take-home pay.

    The pension is treated as salary sacrifice, so it comes off
    the salary before tax, National Insurance and student loan.
    """
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    if not 0 <= pension_percent <= 100:
        raise ValueError("Pension must be between 0% and 100%")

    pension = round(salary * pension_percent / 100, 2)
    adjusted = salary - pension
    tax = income_tax(adjusted)
    ni = national_insurance(adjusted)
    loan = student_loan(adjusted, plan)
    net = round(adjusted - tax - ni - loan, 2)

    return {
        "salary": salary,
        "pension": pension,
        "income_tax": tax,
        "national_insurance": ni,
        "student_loan": loan,
        "take_home": net,
    }
