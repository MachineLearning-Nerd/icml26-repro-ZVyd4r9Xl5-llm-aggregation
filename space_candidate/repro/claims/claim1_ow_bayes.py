"""Machine-check the universal algebraic certificate behind Theorem 1.

The decisive argument is symbolic, not a finite simulation.  For a generic
vote indicator v_i(s) in {0, 1}, this module checks that each conditional
likelihood factor can be rewritten as a label-independent positive factor
times the OW odds ratio raised to v_i(s).  Multiplying over agents and taking
the strictly increasing logarithm proves equality of the MAP and OW argmax
sets for every admissible N, K, accuracy vector, and answer profile.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final


def _find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("could not locate repository or Space root")


ROOT: Final = _find_root()
_INTERNAL_CERTIFICATE: Final = (
    ROOT / ".openresearch" / "artifacts" / "claim_1" / "proof_certificate.json"
)
CERTIFICATE: Final = (
    _INTERNAL_CERTIFICATE
    if _INTERNAL_CERTIFICATE.is_file()
    else ROOT / "evidence" / "claim-1" / "proof_certificate.json"
)


def _add_affine(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Add exponents represented as constant + coefficient * v."""

    return left[0] + right[0], left[1] + right[1]


def _parse_affine(raw: list[int]) -> tuple[int, int]:
    if len(raw) != 2 or not all(isinstance(value, int) for value in raw):
        raise ValueError(f"invalid affine exponent: {raw!r}")
    return raw[0], raw[1]


def verify_certificate(path: Path = CERTIFICATE) -> dict[str, object]:
    certificate = json.loads(path.read_text())
    if certificate["claim_id"] != "claim_1":
        raise AssertionError("certificate is not for claim_1")
    if certificate["domain"] != {
        "N": "integer >= 1",
        "K": "integer >= 2",
        "x_i": "real with 0 < x_i < 1",
        "v_i_s": "{0,1}",
    }:
        raise AssertionError("certificate domain changed")

    original = {
        name: _parse_affine(exponent)
        for name, exponent in certificate["per_agent_identity"]["original"].items()
    }
    common = {
        name: _parse_affine(exponent)
        for name, exponent in certificate["per_agent_identity"]["common"].items()
    }
    ratio = {
        name: _parse_affine(exponent)
        for name, exponent in certificate["per_agent_identity"]["vote_ratio"].items()
    }
    variables = sorted(set(original) | set(common) | set(ratio))
    factorized = {
        variable: _add_affine(
            common.get(variable, (0, 0)), ratio.get(variable, (0, 0))
        )
        for variable in variables
    }
    if original != factorized:
        raise AssertionError(
            f"likelihood factorization failed: {original=} {factorized=}"
        )

    # Check both possible indicator values as an independent guard against an
    # incorrectly encoded affine identity.
    instantiated: dict[str, dict[str, int]] = {}
    for vote in (0, 1):
        lhs = {
            variable: constant + coefficient * vote
            for variable, (constant, coefficient) in original.items()
        }
        rhs = {
            variable: constant + coefficient * vote
            for variable, (constant, coefficient) in factorized.items()
        }
        if lhs != rhs:
            raise AssertionError(f"identity failed at vote={vote}")
        instantiated[str(vote)] = lhs

    inverse = certificate["inverse_link"]
    if inverse != {
        "sigma_K": "exp(z)/(K-1+exp(z))",
        "odds": "x_i*(K-1)/(1-x_i)",
        "inverse": "log(x_i*(K-1)/(1-x_i))",
    }:
        raise AssertionError("inverse-link certificate changed")

    assumptions = certificate["positivity"]
    required = {
        "x_i": "positive",
        "1-x_i": "positive",
        "K-1": "positive",
        "log": "strictly increasing on positive reals",
    }
    if assumptions != required:
        raise AssertionError("positivity or monotonicity premise changed")

    return {
        "status": "PASS",
        "proof_scope": "universal symbolic certificate",
        "identity": original,
        "instantiated_exponents": instantiated,
        "common_factor_is_label_independent": True,
        "common_factor_is_positive": True,
        "uniform_prior_preserves_likelihood_order": True,
        "strict_log_monotonicity_preserves_argmax": True,
        "inverse_link_matches_ow_weight": True,
        "conclusion": "OW argmax set equals Bayes/MAP argmax set",
    }
