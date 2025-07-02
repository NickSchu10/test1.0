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

## Web App

A simple Flask web application is provided for calculating discounted cash flow (DCF) values.
Install Flask and run the server:

```bash
pip install Flask
python webapp.py
```

Then open `http://127.0.0.1:5000/` in your browser to access the form. Enter the cash flow
parameters, ticker symbol (optional to fetch current price) and the number of shares to
see the estimated intrinsic value.
