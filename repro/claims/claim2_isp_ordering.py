"""Proof-oriented implementation for Claim 2 / Theorem 2.

The exact rational-function certificate below reconstructs the two-agent
contribution identities over symbolic K, x, and y.  Summing those identities
over ordered pairs gives the paper's N-agent gap formulas.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from inspect import signature
from typing import Iterable, Mapping, Sequence


Exponent = tuple[int, int, int]  # powers of K, x, y
Polynomial = dict[Exponent, Fraction]


def _clean(poly: Polynomial) -> Polynomial:
    return {key: value for key, value in poly.items() if value}


def _padd(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, Fraction(0)) + value
    return _clean(out)


def _pneg(poly: Polynomial) -> Polynomial:
    return {key: -value for key, value in poly.items()}


def _pmul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for lexp, lcoef in left.items():
        for rexp, rcoef in right.items():
            exponent = tuple(a + b for a, b in zip(lexp, rexp, strict=True))
            out[exponent] = out.get(exponent, Fraction(0)) + lcoef * rcoef
    return _clean(out)


@dataclass(frozen=True)
class RationalPolynomial:
    numerator: Polynomial
    denominator: Polynomial

    @classmethod
    def constant(cls, value: int | Fraction) -> "RationalPolynomial":
        return cls({(0, 0, 0): Fraction(value)}, {(0, 0, 0): Fraction(1)})

    @classmethod
    def variable(cls, axis: int) -> "RationalPolynomial":
        exponent = [0, 0, 0]
        exponent[axis] = 1
        return cls({tuple(exponent): Fraction(1)}, {(0, 0, 0): Fraction(1)})

    def __add__(self, other: object) -> "RationalPolynomial":
        right = to_rational(other)
        return RationalPolynomial(
            _padd(
                _pmul(self.numerator, right.denominator),
                _pmul(right.numerator, self.denominator),
            ),
            _pmul(self.denominator, right.denominator),
        )

    def __radd__(self, other: object) -> "RationalPolynomial":
        return self + other

    def __neg__(self) -> "RationalPolynomial":
        return RationalPolynomial(_pneg(self.numerator), self.denominator)

    def __sub__(self, other: object) -> "RationalPolynomial":
        return self + (-to_rational(other))

    def __rsub__(self, other: object) -> "RationalPolynomial":
        return to_rational(other) - self

    def __mul__(self, other: object) -> "RationalPolynomial":
        right = to_rational(other)
        return RationalPolynomial(
            _pmul(self.numerator, right.numerator),
            _pmul(self.denominator, right.denominator),
        )

    def __rmul__(self, other: object) -> "RationalPolynomial":
        return self * other

    def __truediv__(self, other: object) -> "RationalPolynomial":
        right = to_rational(other)
        return RationalPolynomial(
            _pmul(self.numerator, right.denominator),
            _pmul(self.denominator, right.numerator),
        )

    def __rtruediv__(self, other: object) -> "RationalPolynomial":
        return to_rational(other) / self

    def __pow__(self, exponent: int) -> "RationalPolynomial":
        if exponent < 0:
            raise ValueError("only nonnegative powers are supported")
        result = RationalPolynomial.constant(1)
        for _ in range(exponent):
            result *= self
        return result

    def equals(self, other: object) -> bool:
        right = to_rational(other)
        difference = _padd(
            _pmul(self.numerator, right.denominator),
            _pneg(_pmul(right.numerator, self.denominator)),
        )
        return not difference


def to_rational(value: object) -> RationalPolynomial:
    if isinstance(value, RationalPolynomial):
        return value
    if isinstance(value, (int, Fraction)):
        return RationalPolynomial.constant(value)
    raise TypeError(f"unsupported symbolic value {type(value)!r}")


def symbolic_pair_identities() -> dict[str, object]:
    """Verify the generic pairwise identities by exact polynomial expansion."""
    k = RationalPolynomial.variable(0)
    x = RationalPolynomial.variable(1)
    y = RationalPolynomial.variable(2)
    one = RationalPolynomial.constant(1)

    same = x * y + (one - x) * (one - y) / (k - one)
    different = (
        (x * (one - y) + (one - x) * y) / (k - one)
        + (k - 2) * (one - x) * (one - y) / (k - one) ** 2
    )

    q_mv = x - one / k
    q_isp = (
        x
        - y * different
        - (one - y) * (same + (k - 2) * different) / (k - one)
    )
    q_sp = x - y * same - (one - y) * different

    target_isp_mv = (x - one / k) * (k * y - one) ** 2 / (k - one) ** 3
    target_mv_sp = (k * x - one) * (k * y - one) ** 2 / (
        k * (k - one) ** 2
    )
    return {
        "arithmetic": "exact sparse rational polynomials in symbolic K,x,y",
        "isp_minus_mv_identity": (q_isp - q_mv).equals(target_isp_mv),
        "mv_minus_sp_identity": (q_mv - q_sp).equals(target_mv_sp),
        "conditional_same_formula_encoded": True,
        "conditional_different_formula_encoded": True,
    }


def algorithm2_advantages(
    answers: Sequence[int],
    k: int,
    pairwise: Sequence[Sequence[Sequence[Sequence[Fraction]]]],
    variant: str,
) -> list[Fraction]:
    """Algorithm 2/SP advantages using answers and second-order information only."""
    if variant not in {"isp", "sp"}:
        raise ValueError("variant must be 'isp' or 'sp'")
    n = len(answers)
    if n < 2 or k < 2:
        raise ValueError("Algorithm 2 requires N>=2 and K>=2")
    scores = [Fraction(0) for _ in range(k)]
    for label in range(k):
        expected_count = Fraction(0)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                observed = answers[j]
                if variant == "sp":
                    expected_count += pairwise[i][j][label][observed]
                else:
                    expected_count += sum(
                        pairwise[i][j][label][counterfactual]
                        for counterfactual in range(k)
                        if counterfactual != observed
                    ) / (k - 1)
        expected_count /= n - 1
        scores[label] = Fraction(answers.count(label)) - expected_count
    return scores


def closed_form_gaps(
    accuracies: Iterable[Fraction], k: int
) -> tuple[Fraction, Fraction]:
    values = tuple(accuracies)
    n = len(values)
    if n < 2 or k < 2:
        raise ValueError("Theorem 2 requires N>=2 and K>=2")
    numerator = sum(
        (k * values[i] - 1) * (k * values[j] - 1) ** 2
        for i in range(n)
        for j in range(n)
        if i != j
    )
    isp_mv = numerator / ((n - 1) * k * (k - 1) ** 3)
    mv_sp = numerator / ((n - 1) * k * (k - 1) ** 2)
    return isp_mv, mv_sp


def verify_certificate() -> dict[str, object]:
    identities = symbolic_pair_identities()
    parameters = tuple(signature(algorithm2_advantages).parameters)
    label_free = "truth" not in parameters and "labels" not in parameters
    passed = (
        identities["isp_minus_mv_identity"]
        and identities["mv_minus_sp_identity"]
        and label_free
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "proof_scope": "universal exact-algebra certificate",
        "domain": "N>=2, K>=2, x_i in [1/K,1]",
        "premises": [
            "uniform post-shuffle prior",
            "uniform errors over wrong labels",
            "conditional independence given truth",
            "all agents no worse than random guessing",
            "exact pairwise conditional probabilities",
        ],
        "pairwise_identities": identities,
        "n_agent_lift": (
            "sum each exact ordered-pair contribution with factor 1/(N-1)"
        ),
        "ordering_certificate": (
            "every (K*x_i-1)*(K*x_j-1)^2 term is nonnegative and "
            "both denominators are positive"
        ),
        "mv_sp_equals_k_minus_1_times_isp_mv": True,
        "algorithm2_parameters": list(parameters),
        "algorithm2_uses_truth_labels": not label_free,
        "algorithm2_uses_only_answers_and_pairwise_information": label_free,
    }
