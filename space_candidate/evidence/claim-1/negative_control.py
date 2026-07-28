"""Conditional-dependence control that must make OW disagree with MAP."""

from __future__ import annotations

import json
from fractions import Fraction


ERROR_PROBABILITY = {
    (0, 0, 0): Fraction(56, 100),
    (0, 0, 1): Fraction(1, 100),
    (0, 1, 0): Fraction(2, 100),
    (0, 1, 1): Fraction(11, 100),
    (1, 0, 0): Fraction(2, 100),
    (1, 0, 1): Fraction(11, 100),
    (1, 1, 0): Fraction(10, 100),
    (1, 1, 1): Fraction(7, 100),
}


def main() -> int:
    total = sum(ERROR_PROBABILITY.values(), Fraction())
    error_rates = [
        sum(
            probability
            for error, probability in ERROR_PROBABILITY.items()
            if error[agent] == 1
        )
        for agent in range(3)
    ]
    accuracies = [1 - rate for rate in error_rates]

    # With truth 0, answers equal the error vector. With truth 1, answers are
    # the bitwise complement of the error vector.
    answers = (0, 0, 1)
    likelihood_truth_0 = ERROR_PROBABILITY[answers]
    complement = tuple(1 - answer for answer in answers)
    likelihood_truth_1 = ERROR_PROBABILITY[complement]
    map_label = 0 if likelihood_truth_0 > likelihood_truth_1 else 1

    odds = [accuracy / (1 - accuracy) for accuracy in accuracies]
    ow_score_0 = odds[0] * odds[1]
    ow_score_1 = odds[2]
    ow_label = 0 if ow_score_0 > ow_score_1 else 1

    passed = (
        total == 1
        and accuracies == [Fraction(7, 10)] * 3
        and map_label == 1
        and ow_label == 0
    )
    output = {
        "status": "PASS" if passed else "FAIL",
        "purpose": "Assumption 1 violation must break OW/MAP equivalence",
        "uniform_prior_preserved": True,
        "marginal_accuracies": [str(value) for value in accuracies],
        "conditional_independence": False,
        "witness_answers": answers,
        "P_answers_given_truth_0": str(likelihood_truth_0),
        "P_answers_given_truth_1": str(likelihood_truth_1),
        "map_label": map_label,
        "ow_label": ow_label,
        "expected_disagreement_observed": map_label != ow_label,
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
