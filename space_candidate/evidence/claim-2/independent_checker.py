"""Independent exact checker for Claim 2; imports no production code."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


def response_probability(
    answer: int, truth: int, accuracy: Fraction, k: int
) -> Fraction:
    return accuracy if answer == truth else (1 - accuracy) / (k - 1)


def pairwise_information(
    accuracies: tuple[Fraction, ...], k: int
) -> list[list[list[list[Fraction]]]]:
    n = len(accuracies)
    output = [
        [
            [[Fraction(0) for _ in range(k)] for _ in range(k)]
            for _ in range(n)
        ]
        for _ in range(n)
    ]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for label in range(k):
                for observed in range(k):
                    # P(A_j=observed)=1/K, so the uniform-prior factors cancel.
                    output[i][j][label][observed] = sum(
                        response_probability(label, truth, accuracies[i], k)
                        * response_probability(observed, truth, accuracies[j], k)
                        for truth in range(k)
                    )
    return output


def advantages(
    answers: tuple[int, ...],
    k: int,
    pairwise: list[list[list[list[Fraction]]]],
    variant: str,
) -> list[Fraction]:
    n = len(answers)
    scores = [Fraction(0) for _ in range(k)]
    for label in range(k):
        predicted = Fraction(0)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if variant == "mv":
                    continue
                if variant == "sp":
                    predicted += pairwise[i][j][label][answers[j]]
                else:
                    predicted += sum(
                        pairwise[i][j][label][alternative]
                        for alternative in range(k)
                        if alternative != answers[j]
                    ) / (k - 1)
        if variant == "mv":
            predicted = Fraction(n, k)
        else:
            predicted /= n - 1
        scores[label] = Fraction(answers.count(label)) - predicted
    return scores


def expected_true_advantages(
    accuracies: tuple[Fraction, ...], k: int
) -> dict[str, Fraction]:
    n = len(accuracies)
    pairwise = pairwise_information(accuracies, k)
    output = {name: Fraction(0) for name in ("isp", "mv", "sp")}
    for truth in range(k):
        for answers in itertools.product(range(k), repeat=n):
            probability = Fraction(1, k)
            for i, answer in enumerate(answers):
                probability *= response_probability(
                    answer, truth, accuracies[i], k
                )
            for name in output:
                output[name] += probability * advantages(
                    answers, k, pairwise, name
                )[truth]
    return output


def closed_form(
    accuracies: tuple[Fraction, ...], k: int
) -> tuple[Fraction, Fraction]:
    n = len(accuracies)
    numerator = sum(
        (k * accuracies[i] - 1) * (k * accuracies[j] - 1) ** 2
        for i in range(n)
        for j in range(n)
        if i != j
    )
    return (
        numerator / ((n - 1) * k * (k - 1) ** 3),
        numerator / ((n - 1) * k * (k - 1) ** 2),
    )


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> int:
    cases = [
        (2, (Fraction(1, 2), Fraction(3, 4))),
        (2, (Fraction(2, 3), Fraction(3, 4), Fraction(4, 5))),
        (3, (Fraction(1, 3), Fraction(1, 2), Fraction(4, 5))),
        (4, (Fraction(1, 4), Fraction(3, 5))),
    ]
    results = []
    all_pass = True
    total_profiles = 0
    for k, accuracies in cases:
        observed = expected_true_advantages(accuracies, k)
        formula_isp_mv, formula_mv_sp = closed_form(accuracies, k)
        exact_match = (
            observed["isp"] - observed["mv"] == formula_isp_mv
            and observed["mv"] - observed["sp"] == formula_mv_sp
        )
        ordering = observed["isp"] >= observed["mv"] >= observed["sp"]
        case_profiles = k ** len(accuracies)
        total_profiles += case_profiles
        all_pass = all_pass and exact_match and ordering
        results.append(
            {
                "K": k,
                "N": len(accuracies),
                "accuracies": [fraction_text(value) for value in accuracies],
                "profiles_exhausted": case_profiles,
                "expected_advantage": {
                    name: fraction_text(value)
                    for name, value in observed.items()
                },
                "observed_isp_minus_mv": fraction_text(
                    observed["isp"] - observed["mv"]
                ),
                "formula_isp_minus_mv": fraction_text(formula_isp_mv),
                "observed_mv_minus_sp": fraction_text(
                    observed["mv"] - observed["sp"]
                ),
                "formula_mv_minus_sp": fraction_text(formula_mv_sp),
                "exact_formula_match": exact_match,
                "ordering": ordering,
            }
        )
    output = {
        "status": "PASS" if all_pass else "FAIL",
        "arithmetic": "fractions.Fraction",
        "imports_production_aggregation": False,
        "aggregation_inputs": ["answers", "K", "pairwise conditionals"],
        "aggregation_receives_ground_truth": False,
        "cases": results,
        "total_answer_profiles_exhausted": total_profiles,
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
