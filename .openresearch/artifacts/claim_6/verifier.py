"""Claim 6 universal certificate; exits nonzero on any proof/control failure."""

from __future__ import annotations

import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


def find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("could not locate repository root")


ROOT = find_root()
sys.path.insert(0, str(ROOT))

from repro.claims.claim6_bt import controls, numerical_examples, symbolic_certificate


def git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    started = time.perf_counter()
    artifact_dir = Path(__file__).resolve().parent
    certificate = symbolic_certificate()
    examples = numerical_examples()
    control = controls()
    independent_process = subprocess.run(
        [sys.executable, str(artifact_dir / "independent_checker.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    independent = json.loads(independent_process.stdout)
    example_pass = all(
        math.isclose(row["sigmoid_of_weight"], row["accuracy"], abs_tol=1e-14)
        and math.isclose(
            row["bt_probability_with_shifted_scores"],
            row["accuracy"],
            abs_tol=1e-14,
        )
        for row in examples
    )
    controls_pass = (
        control["wrong_log_probability_transform_rejected"]
        and all(control["finite_domain_endpoint_rejections"].values())
        and control["positive_common_scale_preserves_argmax"]
        and control["negative_common_scale_reverses_argmax"]
    )
    certificate_pass = (
        certificate["status"] == "PASS"
        and certificate["denominator_positive"]
        and certificate["solution_positive"]
        and certificate["solution_unique"]
    )
    independent_pass = (
        independent_process.returncode == 0 and independent["status"] == "PASS"
    )
    passed = certificate_pass and example_pass and controls_pass and independent_pass
    output = {
        "claim_id": "claim_6",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "status": "PASS" if passed else "FAIL",
        "proof_scope": "universal symbolic identity for every x in (0,1)",
        "symbolic_certificate": certificate,
        "numerical_examples": examples,
        "independent_checker": independent,
        "negative_controls": control,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_count_visible": os.cpu_count(),
        "configured_workers": 1,
        "stochastic": False,
        "seed": None,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("CLAIM_6_RESULT=" + json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
