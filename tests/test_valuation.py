import math
from stock_analysis.valuation import compute_intrinsic_value


def test_intrinsic_value_no_growth():
    cash_flows = [100, 110, 121]
    discount_rate = 0.1
    # PV = 100/1.1 + 110/1.1^2 + 121/1.1^3 + terminal using last CF with zero growth
    expected = (
        cash_flows[0] / 1.1
        + cash_flows[1] / 1.1**2
        + cash_flows[2] / 1.1**3
        + cash_flows[2] / 0.1 / 1.1**3
    )
    result = compute_intrinsic_value(cash_flows, discount_rate, terminal_growth_rate=0.0)
    assert math.isclose(result, expected, rel_tol=1e-9)
