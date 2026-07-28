"""Control: violate the no-worse-than-chance premise and require reversal."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path


CHECKER_PATH = Path(__file__).with_name("independent_checker.py")
SPEC = importlib.util.spec_from_file_location("claim2_independent", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load independent checker")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def main() -> int:
    k = 2
    accuracies = (Fraction(2, 5), Fraction(9, 10))
    observed = CHECKER.expected_true_advantages(accuracies, k)
    reversed_isp_mv = observed["isp"] < observed["mv"]
    reversed_mv_sp = observed["mv"] < observed["sp"]
    passed = reversed_isp_mv and reversed_mv_sp
    output = {
        "status": "PASS" if passed else "FAIL",
        "purpose": (
            "the ordering must fail when the no-worse-than-random premise "
            "is deliberately violated"
        ),
        "K": k,
        "N": len(accuracies),
        "accuracies": ["2/5", "9/10"],
        "conditional_independence": True,
        "uniform_post_shuffle_prior": True,
        "uniform_wrong_labels": True,
        "all_agents_at_least_random_chance": False,
        "expected_advantage": {
            name: CHECKER.fraction_text(value)
            for name, value in observed.items()
        },
        "isp_below_mv_observed": reversed_isp_mv,
        "mv_below_sp_observed": reversed_mv_sp,
        "interpretation": "scope control, not a falsification of Theorem 2",
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
