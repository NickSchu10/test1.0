"""Basic discounted cash flow valuation utilities."""

from __future__ import annotations

import argparse
import json
from typing import Iterable, List, Optional
from urllib.request import urlopen


def project_fcfs(initial_fcf: float, growth_rate: float, years: int) -> List[float]:
    """Project free cash flows over a number of years."""
    fcfs = []
    fcf = initial_fcf
    for _ in range(years):
        fcfs.append(fcf)
        fcf *= 1 + growth_rate
    return fcfs


def present_value(cashflows: Iterable[float], discount_rate: float) -> float:
    """Discount a series of cash flows to present value."""
    pv = 0.0
    for i, cf in enumerate(cashflows, start=1):
        pv += cf / (1 + discount_rate) ** i
    return pv


def terminal_value(last_fcf: float, discount_rate: float, terminal_growth: float) -> float:
    """Calculate a terminal value using the Gordon growth model."""
    return last_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)


def fetch_price(ticker: str) -> Optional[float]:
    """Fetch the current market price using Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    try:
        with urlopen(url) as resp:
            data = json.load(resp)
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except Exception:
        return None


def compute_intrinsic_value(
    initial_fcf: float,
    growth_rate: float,
    discount_rate: float,
    years: int,
    terminal_growth: float,
) -> float:
    """Compute the intrinsic value of a firm using DCF."""
    fcfs = project_fcfs(initial_fcf, growth_rate, years)
    pv_fcfs = present_value(fcfs, discount_rate)
    tv = terminal_value(fcfs[-1], discount_rate, terminal_growth)
    pv_tv = tv / (1 + discount_rate) ** years
    return pv_fcfs + pv_tv


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Simple DCF valuation")
    parser.add_argument("--fcf", type=float, required=True, help="Current free cash flow")
    parser.add_argument("--growth", type=float, default=0.02, help="FCF growth rate")
    parser.add_argument("--discount", type=float, default=0.1, help="Discount rate")
    parser.add_argument("--years", type=int, default=5, help="Projection years")
    parser.add_argument("--terminal-growth", type=float, default=0.02, help="Terminal growth rate")
    parser.add_argument("--ticker", help="Ticker symbol to fetch current price")
    parser.add_argument("--shares", type=float, help="Shares outstanding for per-share value")
    args = parser.parse_args(argv)

    intrinsic = compute_intrinsic_value(
        args.fcf, args.growth, args.discount, args.years, args.terminal_growth
    )

    if args.shares:
        intrinsic_per_share = intrinsic / args.shares
        print(f"Intrinsic value per share: {intrinsic_per_share:.2f}")
    else:
        print(f"Intrinsic firm value: {intrinsic:.2f}")

    if args.ticker:
        price = fetch_price(args.ticker)
        if price is None:
            print("Could not fetch current market price.")
        else:
            if args.shares:
                print(f"Current price: {price:.2f}")
                diff = intrinsic_per_share - price
                print(f"Difference: {diff:.2f}")
            else:
                market_val = price * args.shares if args.shares else price
                diff = intrinsic - market_val
                print(f"Current market value: {market_val:.2f}")
                print(f"Difference: {diff:.2f}")


if __name__ == "__main__":
    main()
