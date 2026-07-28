#!/usr/bin/env python3
"""Verify the completeness and honesty of the Claim 4 BLOCKED verdict."""

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

from repro.claims.claim4_real_data import (  # noqa: E402
    EXPECTED,
    REQUIRED_CAPABILITIES,
    all_published_ow_l_lifts_positive,
    faithful_rerun_ready,
    table_matches_exact_contract,
)

HERE = Path(__file__).resolve().parent


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
    table = json.loads((HERE / "published_table3.json").read_text(encoding="utf-8"))
    routes = json.loads((HERE / "route_evidence.json").read_text(encoding="utf-8"))
    discovery = json.loads((HERE / "public_discovery.json").read_text(encoding="utf-8"))

    checker = subprocess.run(
        [sys.executable, str(HERE / "independent_checker.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    checker_output = json.loads(checker.stdout)

    route_rows = routes["routes"]
    route_ids = [row["route_id"] for row in route_rows]
    distinct_methods = {row["method"] for row in route_rows}
    capabilities = routes["required_capabilities"]
    ready = faithful_rerun_ready(capabilities)

    table_only_capabilities = {name: False for name in REQUIRED_CAPABILITIES}
    table_only_rejected = not faithful_rerun_ready(table_only_capabilities)
    falsification = route_rows[-1]

    checks = {
        "exact_contract_matches_source_table": table_matches_exact_contract(table),
        "all_three_published_lifts_positive": all_published_ow_l_lifts_positive(table),
        "four_routes_recorded_in_required_order": route_ids
        == [
            "route_1_release_discovery",
            "route_2_faithful_regeneration",
            "route_3_aggregate_reconstruction",
            "route_4_assumption_matching_falsification",
        ],
        "four_materially_distinct_methods": len(distinct_methods) == 4,
        "each_route_records_interpretation_command_result_and_control": all(
            all(row.get(field) for field in ("interpretation", "commands", "result", "control"))
            for row in route_rows
        ),
        "first_three_routes_unresolved": all(
            row["resolved"] is False for row in route_rows[:3]
        ),
        "mandatory_fourth_route_is_falsification": falsification["route_id"].startswith(
            "route_4"
        ),
        "no_invalid_falsification_claimed": falsification["valid_counterexample_found"]
        is False,
        "all_required_capability_keys_present": set(capabilities)
        == set(REQUIRED_CAPABILITIES),
        "faithful_rerun_not_ready": not ready,
        "table_only_negative_control_rejected": table_only_rejected,
        "independent_checker_passes": checker.returncode == 0
        and checker_output["status"] == "PASS",
        "public_search_has_positive_dataset_controls": all(
            discovery["public_dataset_controls"][name]["search_result_count"] > 0
            for name in ("UltraFeedback", "MMLU")
        ),
        "verdict_is_blocked": routes["verdict"] == "BLOCKED",
        "concrete_unblocker_recorded": bool(routes["unblocker"]),
    }

    result = {
        "claim_id": "claim_4",
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "configured_workers": 1,
        "cpu_count_visible": os.cpu_count(),
        "stochastic": False,
        "paper_values": EXPECTED,
        "routes": route_rows,
        "required_capabilities": capabilities,
        "independent_checker": checker_output,
        "negative_control": {
            "purpose": "published aggregates alone must never be accepted as raw reproduction evidence",
            "table_only_bundle_rejected": table_only_rejected,
            "status": "PASS" if table_only_rejected else "FAIL",
        },
        "checks": checks,
        "audit_status": "PASS" if all(checks.values()) else "FAIL",
        "verdict": "BLOCKED",
        "unblocker": routes["unblocker"],
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("CLAIM_4_RESULT=" + json.dumps(result, sort_keys=True))
    return 0 if result["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
