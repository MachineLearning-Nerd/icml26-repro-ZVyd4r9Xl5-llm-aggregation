"""Independent integer-arithmetic checker for Claim 5; imports no production code."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def main() -> int:
    path = Path(__file__).resolve().parent / "raw" / "appendix_tables_4_6.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    def bp(value: str) -> int:
        whole, fraction = value.split(".")
        return int(whole) * 100 + int(fraction.ljust(2, "0"))

    wins = sum(bp(row["ow_l"]) > bp(row["mv"]) for row in rows)
    lifts = [
        max(bp(row["ow_l"]), bp(row["ow_i"]), bp(row["isp"])) - bp(row["mv"])
        for row in rows
    ]
    per_dataset = {}
    for dataset in sorted({row["dataset"] for row in rows}):
        subset = [row for row in rows if row["dataset"] == dataset]
        per_dataset[dataset] = {
            "rows": len(subset),
            "unique_ensembles": len({row["ensemble"] for row in subset}),
            "owl_wins": sum(bp(row["ow_l"]) > bp(row["mv"]) for row in subset),
        }
    passed = (
        len(rows) == 48
        and wins == 47
        and min(lifts) == 54
        and max(lifts) == 1420
        and all(item["rows"] == item["unique_ensembles"] == 16 for item in per_dataset.values())
    )
    output = {
        "checker": "independent integer hundredths-of-percentage-point route",
        "rows": len(rows),
        "owl_wins": wins,
        "owl_fraction": f"{wins}/48",
        "owl_percent": round(100 * wins / 48, 2),
        "best_lift_min_hundredths_pp": min(lifts),
        "best_lift_max_hundredths_pp": max(lifts),
        "per_dataset": per_dataset,
        "status": "PASS" if passed else "FAIL",
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
