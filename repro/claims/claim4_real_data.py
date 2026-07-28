"""Claim 4: exact Table 3 contract and evidence-readiness audit."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


EXPECTED = {
    "UltraFeedback": {
        "retained_examples": 56_380,
        "K": 2,
        "ow_l": "73.66",
        "mv": "72.21",
    },
    "MMLU": {
        "retained_examples": 109_820,
        "K": 4,
        "ow_l": "90.37",
        "mv": "89.32",
    },
    "ARMMAN": {
        "retained_examples": 11_785,
        "K": 2,
        "ow_l": "85.78",
        "mv": "85.24",
    },
}

REQUIRED_CAPABILITIES = (
    "exact_retained_row_ids",
    "exact_shuffle_maps",
    "exact_strong_model_predictions",
    "armman_records_and_labels",
    "gpt_azure_deployment_access",
    "paper_ow_l_implementation",
)


def rounded_count_candidates(n: int, displayed_percent: str) -> list[int]:
    """Integer correct counts that half-up round to a displayed percentage."""
    target = Decimal(displayed_percent)
    quantum = Decimal("0.01")
    return [
        correct
        for correct in range(n + 1)
        if (Decimal(100) * correct / n).quantize(
            quantum, rounding=ROUND_HALF_UP
        )
        == target
    ]


def table_matches_exact_contract(table: dict[str, dict[str, object]]) -> bool:
    return all(
        dataset in table
        and int(table[dataset]["retained_examples"]) == expected["retained_examples"]
        and int(table[dataset]["K"]) == expected["K"]
        and str(table[dataset]["ow_l"]) == expected["ow_l"]
        and str(table[dataset]["mv"]) == expected["mv"]
        for dataset, expected in EXPECTED.items()
    )


def faithful_rerun_ready(capabilities: dict[str, bool]) -> bool:
    return all(capabilities.get(name) is True for name in REQUIRED_CAPABILITIES)


def all_published_ow_l_lifts_positive(
    table: dict[str, dict[str, object]],
) -> bool:
    return all(
        Decimal(str(row["ow_l"])) > Decimal(str(row["mv"]))
        for row in table.values()
    )
