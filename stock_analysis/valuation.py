"""Valuation utilities for stock analysis."""

from typing import List


def compute_intrinsic_value(
    cash_flows: List[float],
    discount_rate: float,
    terminal_growth_rate: float = 0.0,
) -> float:
    """Compute the present value of future cash flows using a DCF model."""
    if discount_rate <= terminal_growth_rate:
        raise ValueError("discount_rate must be greater than terminal_growth_rate")

    value = 0.0
    for t, cf in enumerate(cash_flows, start=1):
        value += cf / (1 + discount_rate) ** t

    if cash_flows:
        last_cf = cash_flows[-1]
        terminal_value = last_cf * (1 + terminal_growth_rate) / (
            discount_rate - terminal_growth_rate
        )
        value += terminal_value / (1 + discount_rate) ** len(cash_flows)

    return value
