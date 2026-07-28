"""Exact Appendix E.4 aggregate audit for Claim 5."""

from __future__ import annotations

import csv
import hashlib
from decimal import Decimal
from itertools import product
from pathlib import Path

EXPECTED_DATASETS = {"UltraFeedback", "MMLU", "ARMMAN"}
EXPECTED_ENSEMBLES = {
    f"G{g}, Q{q}, L{l}, P{p}"
    for g, q, l, p in product("SW", repeat=4)
}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    datasets = {row["dataset"] for row in rows}
    ensembles_by_dataset = {
        dataset: {row["ensemble"] for row in rows if row["dataset"] == dataset}
        for dataset in datasets
    }
    complete_design = (
        len(rows) == 48
        and datasets == EXPECTED_DATASETS
        and all(ensembles == EXPECTED_ENSEMBLES for ensembles in ensembles_by_dataset.values())
    )

    owl_wins = sum(Decimal(row["ow_l"]) > Decimal(row["mv"]) for row in rows)
    best_lifts = [
        max(Decimal(row[name]) for name in ("ow_l", "ow_i", "isp"))
        - Decimal(row["mv"])
        for row in rows
    ]
    owl_lifts = [Decimal(row["ow_l"]) - Decimal(row["mv"]) for row in rows]
    strong = {
        row["dataset"]: row
        for row in rows
        if row["ensemble"] == "GS, QS, LS, PS"
    }
    return {
        "row_count": len(rows),
        "datasets": sorted(datasets),
        "rows_per_dataset": {
            dataset: sum(row["dataset"] == dataset for row in rows)
            for dataset in sorted(datasets)
        },
        "complete_2x2x2x2_design": complete_design,
        "owl_win_count": owl_wins,
        "owl_case_count": len(rows),
        "owl_win_percent": str((Decimal(100) * owl_wins / len(rows)).quantize(Decimal("0.01"))),
        "best_method_lift_min_percentage_points": str(min(best_lifts)),
        "best_method_lift_max_percentage_points": str(max(best_lifts)),
        "owl_signed_lift_min_percentage_points": str(min(owl_lifts)),
        "owl_signed_lift_max_percentage_points": str(max(owl_lifts)),
        "strong_ensemble": {
            dataset: {
                name: strong[dataset][name]
                for name in ("ow_l", "ow_i", "isp", "mv")
            }
            for dataset in sorted(strong)
        },
    }


def accepted(summary: dict[str, object]) -> bool:
    return (
        summary["row_count"] == 48
        and summary["complete_2x2x2x2_design"]
        and summary["owl_win_count"] == 47
        and summary["owl_win_percent"] == "97.92"
        and summary["best_method_lift_min_percentage_points"] == "0.54"
        and summary["best_method_lift_max_percentage_points"] == "14.20"
    )


def negative_controls(rows: list[dict[str, str]]) -> dict[str, object]:
    count_mutation = [dict(row) for row in rows]
    for row in count_mutation:
        if Decimal(row["ow_l"]) > Decimal(row["mv"]):
            row["ow_l"] = row["mv"]
            break
    count_summary = summarize(count_mutation)

    range_mutation = [dict(row) for row in rows]
    max_row = max(
        range_mutation,
        key=lambda row: max(Decimal(row[name]) for name in ("ow_l", "ow_i", "isp"))
        - Decimal(row["mv"]),
    )
    max_row["ow_l"] = max_row["mv"]
    range_summary = summarize(range_mutation)

    original = summarize(rows)
    quantifier_control_rejects_conflation = (
        original["owl_signed_lift_min_percentage_points"] != "0.54"
        and original["owl_signed_lift_max_percentage_points"] == "14.20"
    )
    return {
        "count_mutation_rejected": not accepted(count_summary),
        "count_mutation_owl_wins": count_summary["owl_win_count"],
        "range_mutation_rejected": not accepted(range_summary),
        "range_mutation_best_max": range_summary["best_method_lift_max_percentage_points"],
        "owl_only_range_conflation_rejected": quantifier_control_rejects_conflation,
        "owl_only_signed_range": [
            original["owl_signed_lift_min_percentage_points"],
            original["owl_signed_lift_max_percentage_points"],
        ],
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
