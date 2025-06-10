"""Simple stock analysis tools using only the Python standard library."""

import csv
from pathlib import Path
from typing import List


def read_prices(csv_path: Path) -> List[float]:
    """Read closing prices from a CSV file.

    The column containing closing prices is matched in a case-insensitive
    manner so both ``close`` and ``Close`` are accepted.
    """
    prices = []
    with csv_path.open() as f:
        reader = csv.DictReader(f)

        # Determine the correct column name for closing prices
        close_field = None
        if reader.fieldnames:
            for field in reader.fieldnames:
                if field.lower() == "close":
                    close_field = field
                    break

        if close_field is None:
            # If no appropriate column is found, return empty list
            return prices

        for row in reader:
            try:
                price = float(row[close_field])
            except (KeyError, ValueError):
                continue
            prices.append(price)
    return prices


def moving_average(prices: List[float], window: int) -> List[float]:
    """Calculate a simple moving average for a given window size."""
    if window <= 0:
        raise ValueError("window must be > 0")
    if len(prices) < window:
        return []
    avgs = []
    for i in range(window - 1, len(prices)):
        window_prices = prices[i - window + 1 : i + 1]
        avgs.append(sum(window_prices) / window)
    return avgs


def main(csv_file: str, window: int = 5) -> None:
    path = Path(csv_file)
    prices = read_prices(path)
    if not prices:
        print("No valid closing prices found.")
        return
    ma = moving_average(prices, window)
    print(f"Calculated {len(ma)} moving-average values with window={window}.")
    for i, value in enumerate(ma, start=window):
        print(f"Day {i}: {value:.2f}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple stock analysis")
    parser.add_argument("csv_file", help="CSV file with a 'close' column")
    parser.add_argument(
        "--window",
        type=int,
        default=5,
        help="Moving average window size (default: 5)",
    )
    args = parser.parse_args()
    main(args.csv_file, args.window)
