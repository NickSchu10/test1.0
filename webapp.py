"""Simple Flask web app for computing discounted cash flow values."""

from __future__ import annotations

from flask import Flask, render_template_string, request

from stock_analysis.dcf import compute_intrinsic_value, fetch_price

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<title>DCF Calculator</title>
<h1>Discounted Cash Flow Calculator</h1>
<form method="post">
  <label>Free Cash Flow:
    <input type="number" step="0.01" name="fcf" value="{{ request.form.get('fcf','') }}" required>
  </label><br>
  <label>Growth Rate (%):
    <input type="number" step="0.01" name="growth_rate" value="{{ request.form.get('growth_rate','') }}" required>
  </label><br>
  <label>Discount Rate (%):
    <input type="number" step="0.01" name="discount_rate" value="{{ request.form.get('discount_rate','') }}" required>
  </label><br>
  <label>Projection Years:
    <input type="number" name="years" value="{{ request.form.get('years',5) }}" required>
  </label><br>
  <label>Terminal Growth (%):
    <input type="number" step="0.01" name="terminal_growth" value="{{ request.form.get('terminal_growth',2) }}" required>
  </label><br>
  <label>Ticker (optional):
    <input type="text" name="ticker" value="{{ request.form.get('ticker','') }}">
  </label><br>
  <label>Shares (optional):
    <input type="number" step="0.01" name="shares" value="{{ request.form.get('shares','') }}">
  </label><br>
  <input type="submit" value="Calculate">
</form>
{% if intrinsic_value is not none %}
<h2>Results</h2>
<p>Total intrinsic value: {{ intrinsic_value | round(2) }}</p>
{% if shares %}
<p>Intrinsic value per share: {{ intrinsic_value_per_share | round(2) }}</p>
{% endif %}
{% if price is not none %}
<p>Market price per share: {{ price }}</p>
{% if intrinsic_value_per_share is not none %}
<p>Difference: {{ (intrinsic_value_per_share - price) | round(2) }}</p>
{% endif %}
{% endif %}
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    intrinsic_value = None
    intrinsic_value_per_share = None
    price = None
    shares = None
    if request.method == "POST":
        try:
            fcf = float(request.form["fcf"])
            growth_rate = float(request.form["growth_rate"])
            discount_rate = float(request.form["discount_rate"])
            years = int(request.form["years"])
            terminal_growth = float(request.form["terminal_growth"])
            ticker = request.form.get("ticker", "").strip()
            shares_input = request.form.get("shares", "").strip()

            intrinsic_value = compute_intrinsic_value(
                fcf, growth_rate, discount_rate, years, terminal_growth
            )

            if shares_input:
                shares = float(shares_input)
                if shares:
                    intrinsic_value_per_share = intrinsic_value / shares

            if ticker:
                price = fetch_price(ticker)
        except ValueError:
            intrinsic_value = None
    return render_template_string(
        FORM_HTML,
        intrinsic_value=intrinsic_value,
        intrinsic_value_per_share=intrinsic_value_per_share,
        price=price,
        shares=shares,
    )


if __name__ == "__main__":
    app.run(debug=True)
