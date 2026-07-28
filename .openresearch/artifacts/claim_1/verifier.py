"""Executable Claim 1 verifier; exits nonzero on any evidence failure."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from repro.claims.claim1_ow_bayes import verify_certificate


def run_json_script(path: Path) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


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
    symbolic = verify_certificate()
    independent = run_json_script(artifact_dir / "independent_checker.py")
    control = run_json_script(artifact_dir / "negative_control.py")
    passed = all(
        result["status"] == "PASS"
        for result in (symbolic, independent, control)
    )
    output = {
        "claim_id": "claim_1",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "symbolic_certificate": symbolic,
        "independent_checker": independent,
        "negative_control": control,
        "seed": None,
        "stochastic": False,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_count_visible": os.cpu_count(),
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("CLAIM_1_RESULT=" + json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
