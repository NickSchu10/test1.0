"""Discounted Cash Flow utilities."""

from __future__ import annotations

import json
import urllib.request
from typing import Optional


def compute_intrinsic_value(
    fcf: float,
    growth_rate: float,
    discount_rate: float,
    years: int,
    terminal_growth: float,
) -> float:
    """Compute intrinsic value using a simple DCF model.

    Parameters are expressed as percentages except for `years` and `fcf`.
    For example ``growth_rate=5`` means 5%.
    """
    if years <= 0:
        raise ValueError("years must be > 0")

    growth = growth_rate / 100 if growth_rate > 1 else growth_rate
    discount = discount_rate / 100 if discount_rate > 1 else discount_rate
    terminal = terminal_growth / 100 if terminal_growth > 1 else terminal_growth

    pv = 0.0
    for t in range(1, years + 1):
        future_fcf = fcf * (1 + growth) ** t
        pv += future_fcf / (1 + discount) ** t

    terminal_value = (
        fcf * (1 + growth) ** years * (1 + terminal) / (discount - terminal)
    )
    pv += terminal_value / (1 + discount) ** years
    return pv


def fetch_price(ticker: str) -> Optional[float]:
    """Fetch the current market price for ``ticker`` from Yahoo Finance."""
    url = (
        "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + ticker.upper()
    )
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
    except Exception:
        return None
    results = data.get("quoteResponse", {}).get("result", [])
    if not results:
        return None
    price = results[0].get("regularMarketPrice")
    return float(price) if price is not None else None
