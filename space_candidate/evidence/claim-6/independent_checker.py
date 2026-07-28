"""Independent exact-rational checker for Claim 6; imports no production code."""

from __future__ import annotations

import json
from decimal import Decimal, localcontext
from fractions import Fraction


def main() -> int:
    probabilities = [
        Fraction(1, 1000),
        Fraction(1, 10),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(9, 10),
        Fraction(999, 1000),
    ]
    cases = []
    for probability in probabilities:
        odds = probability / (1 - probability)
        recovered = odds / (1 + odds)
        with localcontext() as context:
            context.prec = 60
            decimal_probability = Decimal(probability.numerator) / Decimal(
                probability.denominator
            )
            score_difference = (
                decimal_probability / (Decimal(1) - decimal_probability)
            ).ln()
            bt_probability = score_difference.exp() / (
                Decimal(1) + score_difference.exp()
            )
            numerical_error = abs(bt_probability - decimal_probability)
        cases.append(
            {
                "probability": f"{probability.numerator}/{probability.denominator}",
                "odds": f"{odds.numerator}/{odds.denominator}",
                "rational_composition_exact": recovered == probability,
                "decimal_bt_error": str(numerical_error),
            }
        )
    passed = all(
        case["rational_composition_exact"]
        and Decimal(case["decimal_bt_error"]) <= Decimal("1e-55")
        for case in cases
    )
    output = {
        "checker": "Fraction algebra plus independent Decimal ln/exp route",
        "imports_production_code": False,
        "cases": cases,
        "status": "PASS" if passed else "FAIL",
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
