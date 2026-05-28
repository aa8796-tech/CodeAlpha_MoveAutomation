from dataclasses import dataclass
from collections.abc import Callable, Iterable
import os
# =========================
# Validation Result
# =========================

@dataclass
class ValidationResult:
    is_valid: bool
    message: str = ""


# =========================
# Types
# =========================

Validator = Callable[[str], ValidationResult]


# =========================
# Validation Engine
# =========================

def validate(
    value: str,
    validators: Iterable[Validator],
    fail_fast: bool = True
) -> list[ValidationResult]:
    """
    Runs a sequence of validation rules over a given input value.

    This function applies each validator to the input string and collects
    validation results. It supports two execution modes:

    1. Fail-fast mode:
       Stops at the first validation failure and returns immediately.

    2. Aggregate mode:
       Runs all validators and returns all validation failures.

    Args:
        value (str):
            The input value to be validated.

        validators (Iterable[Validator]):
            A collection of validator functions. Each validator must accept
            a string and return a ValidationResult.

        fail_fast (bool, optional):
            If True, validation stops at the first failure.
            If False, all validators are executed and all failures are collected.
            Default is True.

    Returns:
        list[ValidationResult]:
            A list of validation results that represent failures.
            If the list is empty, the value is considered valid.
    """

    results = []

    for validator in validators:
        result = validator(value)
      
        if not result.is_valid:
            results.append(result)

            if fail_fast:
                return results

    return results

# =========================
# Input validators
# =========================
def is_not_blank(value: str) -> ValidationResult:
    if not value:
        return ValidationResult(False, "Input must not be blank!")
    return ValidationResult(True)

def is_in_range(min_val: int, max_val: int, custom_error: str = None) -> Validator:
    """Factory: Returns a validator that evaluates if a numeric string falls within a specific range.
    Args:
        min_val (int): The inclusive lower bound of the range.
        max_val (int): The inclusive upper bound of the range.
        custom_error (str, optional): A custom error message if validation fails.

    Returns:
        Validator: A callable function dedicated solely to range boundary checking.
    """
    def validator(value: str) -> ValidationResult:
        numeric_value = int(value)
        if min_val <= numeric_value <= max_val:
            return ValidationResult(True)
        
        error_msg = custom_error or f"Value out of range. Expected between {min_val} and {max_val}."
        return ValidationResult(False, error_msg)
        
    return validator

# =========================
# Domain validators
# =========================
def is_valid_srcdir(value: str) -> ValidationResult:
    """Validator to ensure the input path points to an actual existing directory."""
    if not os.path.exists(value):
        return ValidationResult(False, f"The path '{value}' does not exist.")
    
    if not os.path.isdir(value):
        return ValidationResult(False, f"The path '{value}' is not a directory.")
    
    return ValidationResult(True)
