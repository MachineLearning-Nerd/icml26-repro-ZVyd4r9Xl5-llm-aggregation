"""Claim 5 exact aggregate verifier; exits nonzero on any evidence/control failure."""

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

from repro.claims.claim5_tables import accepted, load_rows, negative_controls, sha256, summarize


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
    artifact_dir = Path(__file__).resolve().parent
    data_path = artifact_dir / "appendix_tables_4_6.csv"
    contract = json.loads((artifact_dir / "claim_contract.json").read_text(encoding="utf-8"))
    rows = load_rows(data_path)
    summary = summarize(rows)
    controls = negative_controls(rows)
    independent_process = subprocess.run(
        [sys.executable, str(artifact_dir / "independent_checker.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    independent = json.loads(independent_process.stdout)
    csv_hash = sha256(data_path)
    controls_pass = all(
        controls[name]
        for name in (
            "count_mutation_rejected",
            "range_mutation_rejected",
            "owl_only_range_conflation_rejected",
        )
    )
    independent_pass = independent_process.returncode == 0 and independent["status"] == "PASS"
    passed = (
        csv_hash == contract["source_table_csv_sha256"]
        and accepted(summary)
        and controls_pass
        and independent_pass
        and independent["owl_wins"] == summary["owl_win_count"]
        and independent["best_lift_min_hundredths_pp"] == 54
        and independent["best_lift_max_hundredths_pp"] == 1420
    )
    output = {
        "claim_id": "claim_5",
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "status": "PASS" if passed else "FAIL",
        "scope": "exact arithmetic reconstruction of all 48 published Appendix E.4 rows",
        "quantifier_note": "97.92%=47/48 OW-L wins; 0.54..14.20 pp is per-row best-of-(OW-L,OW-I,ISP) lift, not OW-L-only lift",
        "source_table_csv_sha256": csv_hash,
        "summary": summary,
        "independent_checker": independent,
        "negative_controls": controls,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_count_visible": os.cpu_count(),
        "configured_workers": 1,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("CLAIM_5_RESULT=" + json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
