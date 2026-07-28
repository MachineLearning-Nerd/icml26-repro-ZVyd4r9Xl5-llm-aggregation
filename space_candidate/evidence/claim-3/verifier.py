"""Claim 3 pilot verifier; exits nonzero on implementation/control failure."""

from __future__ import annotations

import json
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

from repro.claims.claim3_simulation import controls, run_full, small_case_digest


def run_independent(path: Path) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def git_sha() -> str:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode == 0:
        return process.stdout.strip()
    metadata = json.loads(
        (Path(__file__).resolve().parent / "run_metadata.json").read_text(
            encoding="utf-8"
        )
    )
    return str(metadata["git_sha"])


def main() -> int:
    started = time.perf_counter()
    independent = run_independent(
        Path(__file__).resolve().with_name("independent_checker.py")
    )
    production_digest = small_case_digest()
    digest_match = production_digest == independent["digest"]
    control = controls()
    control_pass = (
        control["uniform_pairwise_makes_isp_identical_to_mv"]
        and control["sign_mutation_changes_predictions"]
        and control["sign_mutation_reference_digest"]
        != control["sign_mutation_bad_digest"]
    )
    full = run_full()
    passed = digest_match and control_pass and full["verdict"] == "VERIFIED"
    output = {
        "claim_id": "claim_3",
        "stage": "full",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "full_status": "PASS" if passed else "FAIL",
        "production_small_case_digest": production_digest,
        "independent_checker": independent,
        "production_independent_digest_match": digest_match,
        "negative_controls": control,
        "full": full,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_count_visible": os.cpu_count(),
        "configured_workers": 8,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("CLAIM_3_RESULT=" + json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
