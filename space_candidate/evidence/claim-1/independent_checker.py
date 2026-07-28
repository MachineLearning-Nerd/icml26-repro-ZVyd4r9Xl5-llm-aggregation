"""Exact-rational checker independent of the OW implementation."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


CASES = [
    (2, (Fraction(1, 3),)),
    (2, (Fraction(2, 3), Fraction(3, 4), Fraction(4, 5))),
    (3, (Fraction(1, 5), Fraction(1, 3), Fraction(3, 4))),
    (
        4,
        (
            Fraction(1, 5),
            Fraction(1, 4),
            Fraction(3, 5),
            Fraction(4, 5),
        ),
    ),
    (5, (Fraction(1, 6), Fraction(1, 5), Fraction(5, 6))),
]


def maximizers(scores: list[Fraction]) -> list[int]:
    best = max(scores)
    return [index for index, value in enumerate(scores) if value == best]


def check_case(K: int, accuracies: tuple[Fraction, ...]) -> dict[str, object]:
    mismatches: list[dict[str, object]] = []
    profiles = 0
    for answers in itertools.product(range(K), repeat=len(accuracies)):
        profiles += 1
        likelihoods = []
        ow_products = []
        for label in range(K):
            likelihood = Fraction(1, K)
            product = Fraction(1, 1)
            for answer, accuracy in zip(answers, accuracies, strict=True):
                if answer == label:
                    likelihood *= accuracy
                    product *= accuracy * (K - 1) / (1 - accuracy)
                else:
                    likelihood *= (1 - accuracy) / (K - 1)
            likelihoods.append(likelihood)
            ow_products.append(product)
        map_set = maximizers(likelihoods)
        ow_set = maximizers(ow_products)
        if map_set != ow_set:
            mismatches.append(
                {"answers": answers, "map_set": map_set, "ow_set": ow_set}
            )
    return {
        "K": K,
        "N": len(accuracies),
        "accuracies": [str(value) for value in accuracies],
        "profiles_exhausted": profiles,
        "mismatches": mismatches,
    }


def main() -> int:
    results = [check_case(K, accuracies) for K, accuracies in CASES]
    total_profiles = sum(int(case["profiles_exhausted"]) for case in results)
    total_mismatches = sum(len(case["mismatches"]) for case in results)
    output = {
        "status": "PASS" if total_mismatches == 0 else "FAIL",
        "arithmetic": "fractions.Fraction",
        "imports_production_aggregation": False,
        "cases": results,
        "total_profiles_exhausted": total_profiles,
        "total_mismatches": total_mismatches,
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if total_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
