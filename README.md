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
