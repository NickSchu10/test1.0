# test1.0

This repository contains sample code for experimenting with Codex.

## Stock Analysis Tool

The `stock_analysis` package provides a simple script to compute moving
averages from a CSV file of historical prices. It relies only on the
Python standard library.

### Usage

Prepare a CSV file with at least a `close` column, then run:

```bash
python -m stock_analysis.analysis path/to/data.csv --window 10
```

This will print the moving average for each day after the first
`window` observations.

## DCF Valuation Tool

A simple script for discounted cash flow valuation is provided in
`stock_analysis.dcf`. You can project free cash flows, apply discounting
and a terminal value, and optionally compare the result to the current
market price pulled from Yahoo Finance.

Example usage:

```bash
python -m stock_analysis.dcf --fcf 1e6 --growth 0.03 --discount 0.1 \
    --years 5 --terminal-growth 0.02 --shares 1000000 --ticker AAPL
```

If network access is unavailable, the current price lookup will fail
silently.
