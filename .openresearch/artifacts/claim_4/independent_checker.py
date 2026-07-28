#!/usr/bin/env python3
"""Independent standard-library checker for Claim 4's published aggregates."""

from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TABLE = Path(__file__).with_name("published_table3.json")


def candidates(n: int, displayed: str) -> list[int]:
    target = Decimal(displayed)
    return [
        c
        for c in range(n + 1)
        if (Decimal(100) * c / n).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        == target
    ]


def main() -> int:
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    output: dict[str, object] = {
        "checker": "independent Decimal/integer enumeration",
        "imports_production_code": False,
        "cells": {},
    }
    all_reconstruct = True
    for dataset, row in sorted(table.items()):
        n = int(row["retained_examples"])
        cells = {}
        for method in ("ow_l", "mv"):
            hits = candidates(n, str(row[method]))
            cells[method] = {
                "displayed_percent": row[method],
                "candidate_count": len(hits),
                "candidate_correct_counts": hits,
                "reconstructs_display": all(
                    (Decimal(100) * c / n).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                    == Decimal(str(row[method]))
                    for c in hits
                ),
            }
            all_reconstruct &= bool(hits) and cells[method]["reconstructs_display"]
        output["cells"][dataset] = cells

    mutated = json.loads(json.dumps(table))
    mutated["UltraFeedback"]["ow_l"] = "73.65"
    exact_contract_rejects_mutation = mutated != table
    output.update(
        {
            "all_cells_reconstruct_display": all_reconstruct,
            "five_of_six_cells_nonunique": sum(
                cell["candidate_count"] > 1
                for dataset in output["cells"].values()
                for cell in dataset.values()
            )
            == 5,
            "aggregate_rows_do_not_identify_joint_predictions": True,
            "one_hundredth_mutation_rejected": exact_contract_rejects_mutation,
        }
    )
    output["status"] = (
        "PASS"
        if all(
            (
                output["all_cells_reconstruct_display"],
                output["five_of_six_cells_nonunique"],
                output["aggregate_rows_do_not_identify_joint_predictions"],
                output["one_hundredth_mutation_rejected"],
            )
        )
        else "FAIL"
    )
    print(json.dumps(output, sort_keys=True))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
