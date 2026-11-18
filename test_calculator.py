"""Automated tests. The pipeline runs these on every change."""

import pytest

from calculator import income_tax, national_insurance, student_loan, take_home


# Income tax
def test_no_tax_below_personal_allowance():
    assert income_tax(10_000) == 0


def test_basic_rate_tax():
    assert income_tax(30_000) == 3_486


def test_higher_rate_tax():
    assert income_tax(60_000) == 11_432


def test_personal_allowance_shrinks_above_100k():
    assert income_tax(110_000) == 33_432


def test_additional_rate_tax():
    assert income_tax(150_000) == 53_703


# National Insurance
def test_national_insurance_main_rate():
    assert national_insurance(30_000) == 1_394.40


def test_national_insurance_upper_rate():
    assert national_insurance(60_000) == 3_210.60


# Student loans
def test_no_repayment_below_threshold():
    assert student_loan(24_000, "plan_5") == 0


def test_plan_2_repayment():
    assert student_loan(30_000, "plan_2") == 55.35


def test_plan_5_repayment():
    assert student_loan(30_000, "plan_5") == 450


def test_unknown_plan_is_rejected():
    with pytest.raises(ValueError):
        student_loan(30_000, "plan_9")


# Full take-home calculation
def test_take_home_simple():
    assert take_home(30_000)["take_home"] == 25_119.60


def test_pension_reduces_tax_and_ni():
    result = take_home(30_000, pension_percent=5)
    assert result["pension"] == 1_500
    assert result["income_tax"] == 3_186
    assert result["take_home"] == 24_039.60


def test_negative_salary_is_rejected():
    with pytest.raises(ValueError):
        take_home(-1)
