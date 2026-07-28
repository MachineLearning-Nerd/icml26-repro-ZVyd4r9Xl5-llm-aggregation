"""Calibrated reproduction of the paper's N=4, M=10,000 simulation."""

from __future__ import annotations

import hashlib
import math
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Sequence

import numpy as np


ACCURACIES = np.asarray([0.6, 0.7, 0.8, 0.9], dtype=float)
PILOT_SEEDS = (101, 211, 307, 401, 503, 601, 701, 809)
FULL_SEEDS = tuple(range(1000, 1089))
PAPER_K = (2, 4, 6, 8, 10)
EXTENDED_K = (12, 16, 24, 32)
M_QUESTIONS = 10_000
WORKERS = 8
PAPER_ACCURACY = {
    2: {"mv": 0.8513, "isp": 0.9048},
    4: {"mv": 0.9264, "isp": 0.9445},
    6: {"mv": 0.9422, "isp": 0.9578},
    8: {"mv": 0.9485, "isp": 0.9623},
    10: {"mv": 0.9554, "isp": 0.9649},
}


@dataclass(frozen=True)
class Case:
    seed: int
    k: int
    m: int = M_QUESTIONS


def simulate(case: Case) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(np.random.SeedSequence([case.seed, case.k, case.m]))
    truth = rng.integers(0, case.k, size=case.m)
    answers = np.empty((case.m, len(ACCURACIES)), dtype=np.int16)
    for i, accuracy in enumerate(ACCURACIES):
        correct = rng.random(case.m) < accuracy
        wrong_rank = rng.integers(0, case.k - 1, size=case.m)
        wrong_answer = wrong_rank + (wrong_rank >= truth)
        answers[:, i] = np.where(correct, truth, wrong_answer)
    return truth, answers


def estimate_pairwise(answers: np.ndarray, k: int) -> np.ndarray:
    """Empirical P(A_i=s | A_j=a), using no truth labels."""
    _, n = answers.shape
    pairwise = np.zeros((n, n, k, k), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            joint = np.zeros((k, k), dtype=np.int64)
            np.add.at(joint, (answers[:, i], answers[:, j]), 1)
            denominators = joint.sum(axis=0)
            nonempty = denominators > 0
            pairwise[i, j][:, nonempty] = (
                joint[:, nonempty] / denominators[nonempty][None, :]
            )
            pairwise[i, j][:, ~nonempty] = 1.0 / k
    return pairwise


def counts(answers: np.ndarray, k: int) -> np.ndarray:
    output = np.zeros((answers.shape[0], k), dtype=float)
    rows = np.repeat(np.arange(answers.shape[0]), answers.shape[1])
    np.add.at(output, (rows, answers.reshape(-1)), 1)
    return output


def isp_scores(
    answers: np.ndarray, k: int, pairwise: np.ndarray, sign: int = -1
) -> np.ndarray:
    """Algorithm 2 advantage; sign=+1 is the intentional mutation control."""
    _, n = answers.shape
    predicted = np.zeros((answers.shape[0], k), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            matrix = pairwise[i, j]
            total = matrix.sum(axis=1)
            observed_column = matrix[:, answers[:, j]].T
            predicted += (total[None, :] - observed_column) / (k - 1)
    predicted /= n - 1
    return counts(answers, k) + sign * predicted


def random_argmax(scores: np.ndarray, seed_parts: Sequence[int]) -> np.ndarray:
    rng = np.random.default_rng(np.random.SeedSequence(seed_parts))
    output = np.empty(scores.shape[0], dtype=np.int16)
    for row_index, row in enumerate(scores):
        candidates = np.flatnonzero(row == row.max())
        output[row_index] = rng.choice(candidates)
    return output


def predictions(case: Case) -> dict[str, np.ndarray]:
    truth, answers = simulate(case)
    pairwise = estimate_pairwise(answers, case.k)
    tie_seed = (case.seed, case.k, case.m, 17)
    mv = random_argmax(counts(answers, case.k), tie_seed)
    isp = random_argmax(isp_scores(answers, case.k, pairwise), tie_seed)
    return {"truth": truth, "answers": answers, "mv": mv, "isp": isp}


def run_case(case: Case) -> dict[str, float | int]:
    output = predictions(case)
    mv = float(np.mean(output["mv"] == output["truth"]))
    isp = float(np.mean(output["isp"] == output["truth"]))
    return {
        "seed": case.seed,
        "K": case.k,
        "M": case.m,
        "mv": mv,
        "isp": isp,
        "gap": isp - mv,
    }


def digest_arrays(arrays: Sequence[np.ndarray]) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.dtype).encode())
        digest.update(str(contiguous.shape).encode())
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def small_case_digest() -> str:
    output = predictions(Case(seed=19, k=4, m=256))
    return digest_arrays(
        [output["truth"], output["answers"], output["mv"], output["isp"]]
    )


def controls() -> dict[str, object]:
    case = Case(seed=23, k=4, m=512)
    truth, answers = simulate(case)
    uniform = np.full((4, 4, case.k, case.k), 1.0 / case.k, dtype=float)
    for i in range(4):
        uniform[i, i] = 0
    tie_seed = (case.seed, case.k, case.m, 17)
    mv = random_argmax(counts(answers, case.k), tie_seed)
    uniform_isp = random_argmax(isp_scores(answers, case.k, uniform), tie_seed)

    pairwise = estimate_pairwise(answers, case.k)
    mutated = random_argmax(
        isp_scores(answers, case.k, pairwise, sign=+1), tie_seed
    )
    reference = random_argmax(
        isp_scores(answers, case.k, pairwise, sign=-1), tie_seed
    )
    return {
        "uniform_pairwise_makes_isp_identical_to_mv": bool(
            np.array_equal(uniform_isp, mv)
        ),
        "uniform_pairwise_prediction_mismatches": int(np.sum(uniform_isp != mv)),
        "sign_mutation_changes_predictions": bool(np.any(mutated != reference)),
        "sign_mutation_prediction_mismatches": int(np.sum(mutated != reference)),
        "sign_mutation_reference_digest": digest_arrays([truth, answers, reference]),
        "sign_mutation_bad_digest": digest_arrays([truth, answers, mutated]),
    }


def summarize(rows: list[dict[str, float | int]]) -> dict[str, object]:
    by_k: dict[str, object] = {}
    for k in (*PAPER_K, *EXTENDED_K):
        subset = [row for row in rows if row["K"] == k]
        entry: dict[str, object] = {"replicates": len(subset)}
        for metric in ("mv", "isp", "gap"):
            values = np.asarray([row[metric] for row in subset], dtype=float)
            entry[metric] = {
                "mean": float(values.mean()),
                "sample_std": float(values.std(ddof=1)),
                "mean_ci95_normal": [
                    float(values.mean() - 1.96 * values.std(ddof=1) / math.sqrt(len(values))),
                    float(values.mean() + 1.96 * values.std(ddof=1) / math.sqrt(len(values))),
                ],
                "single_run_min": float(values.min()),
                "single_run_max": float(values.max()),
            }
        if k in PAPER_ACCURACY:
            entry["paper"] = PAPER_ACCURACY[k]
            entry["paper_within_pilot_single_run_range"] = {
                metric: bool(
                    entry[metric]["single_run_min"]
                    <= PAPER_ACCURACY[k][metric]
                    <= entry[metric]["single_run_max"]
                )
                for metric in ("mv", "isp")
            }
        by_k[str(k)] = entry
    return by_k


def calibrated_replicate_count(summary: dict[str, object]) -> dict[str, object]:
    target_halfwidth = 0.001
    standard_deviations = []
    for k in ("2", "4"):
        for metric in ("mv", "isp", "gap"):
            standard_deviations.append(summary[k][metric]["sample_std"])
    worst = max(standard_deviations)
    normal_estimate = math.ceil((1.96 * worst / target_halfwidth) ** 2)
    return {
        "target_mean_ci95_halfwidth": target_halfwidth,
        "calibration_basis": "largest observed pilot standard deviation at K=2 or K=4",
        "largest_pilot_sample_std": worst,
        "normal_approximation_minimum": normal_estimate,
        "recommended_replicates": max(30, normal_estimate),
        "note": "the full-run count is calibrated from observed pilot variance, not a theorem formula",
    }


def scaling_slopes(rows: list[dict[str, float | int]]) -> dict[str, object]:
    slopes = []
    k_values = np.asarray(EXTENDED_K, dtype=float)
    for seed in PILOT_SEEDS:
        gaps = np.asarray(
            [next(row["gap"] for row in rows if row["seed"] == seed and row["K"] == k)
             for k in EXTENDED_K],
            dtype=float,
        )
        if np.all(gaps > 0):
            slopes.append(float(np.polyfit(np.log(k_values), np.log(gaps), 1)[0]))
    values = np.asarray(slopes)
    return {
        "K_values": list(EXTENDED_K),
        "valid_seed_slopes": len(slopes),
        "all_seed_slopes": slopes,
        "mean": float(values.mean()) if len(values) else None,
        "sample_std": float(values.std(ddof=1)) if len(values) > 1 else None,
    }


def run_pilot() -> dict[str, object]:
    cases = [
        Case(seed=seed, k=k)
        for seed in PILOT_SEEDS
        for k in (*PAPER_K, *EXTENDED_K)
    ]
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        rows = list(executor.map(run_case, cases))
    rows.sort(key=lambda row: (row["K"], row["seed"]))
    summary = summarize(rows)
    return {
        "stage": "pilot",
        "verdict": "BLOCKED",
        "reason": "pilot calibrates the full replicate count; it is not final claim evidence",
        "N": 4,
        "M": M_QUESTIONS,
        "accuracies": ACCURACIES.tolist(),
        "paper_K": list(PAPER_K),
        "extended_K": list(EXTENDED_K),
        "seeds": list(PILOT_SEEDS),
        "configured_workers": WORKERS,
        "rows": rows,
        "summary": summary,
        "scaling_pilot": scaling_slopes(rows),
        "calibration": calibrated_replicate_count(summary),
    }


def full_summary(rows: list[dict[str, float | int]]) -> dict[str, object]:
    by_k: dict[str, object] = {}
    for k in (*PAPER_K, *EXTENDED_K):
        subset = [row for row in rows if row["K"] == k]
        entry: dict[str, object] = {"replicates": len(subset)}
        for metric in ("mv", "isp", "gap"):
            values = np.asarray([row[metric] for row in subset], dtype=float)
            mean = float(values.mean())
            standard_deviation = float(values.std(ddof=1))
            entry[metric] = {
                "mean": mean,
                "sample_std": standard_deviation,
                "mean_ci95_normal": [
                    mean - 1.96 * standard_deviation / math.sqrt(len(values)),
                    mean + 1.96 * standard_deviation / math.sqrt(len(values)),
                ],
                "single_run_predictive_interval95": [
                    float(np.quantile(values, 0.025)),
                    float(np.quantile(values, 0.975)),
                ],
                "single_run_min": float(values.min()),
                "single_run_max": float(values.max()),
            }
        if k in PAPER_ACCURACY:
            entry["paper"] = PAPER_ACCURACY[k]
            compatibility = {}
            for metric in ("mv", "isp"):
                paper_value = PAPER_ACCURACY[k][metric]
                observed = entry[metric]
                z_score = (
                    (paper_value - observed["mean"]) / observed["sample_std"]
                    if observed["sample_std"] > 0
                    else 0.0
                )
                low, high = observed["single_run_predictive_interval95"]
                compatibility[metric] = {
                    "single_run_z_score": z_score,
                    "within_empirical_predictive_interval95": bool(
                        low <= paper_value <= high
                    ),
                }
            entry["paper_compatibility"] = compatibility
        by_k[str(k)] = entry
    return by_k


def accuracy_gap_scaling(rows: list[dict[str, float | int]]) -> dict[str, object]:
    k_values = np.asarray(PAPER_K, dtype=float)
    mean_gaps = np.asarray(
        [
            np.mean([row["gap"] for row in rows if row["K"] == k])
            for k in PAPER_K
        ],
        dtype=float,
    )
    seed_slopes = []
    for seed in FULL_SEEDS:
        gaps = np.asarray(
            [
                next(
                    row["gap"]
                    for row in rows
                    if row["seed"] == seed and row["K"] == k
                )
                for k in PAPER_K
            ],
            dtype=float,
        )
        if np.all(gaps > 0):
            seed_slopes.append(
                float(np.polyfit(np.log(k_values), np.log(gaps), 1)[0])
            )
    return {
        "scope": "empirical aggregation-accuracy gap on the paper K grid",
        "K_values": list(PAPER_K),
        "mean_gaps": mean_gaps.tolist(),
        "mean_gap_loglog_slope": float(
            np.polyfit(np.log(k_values), np.log(mean_gaps), 1)[0]
        ),
        "valid_seed_slopes": len(seed_slopes),
        "seed_slope_median": float(np.median(seed_slopes)),
        "seed_slope_interval95": [
            float(np.quantile(seed_slopes, 0.025)),
            float(np.quantile(seed_slopes, 0.975)),
        ],
        "interpretation": (
            "finite-grid empirical evidence only; the paper's exact Theta "
            "statement is for expected advantage"
        ),
    }


def expected_advantage_scaling() -> dict[str, object]:
    k_values = np.asarray([16, 32, 64, 128, 256, 512], dtype=float)
    gaps = []
    n = len(ACCURACIES)
    for k_float in k_values:
        k = int(k_float)
        numerator = sum(
            (k * ACCURACIES[i] - 1) * (k * ACCURACIES[j] - 1) ** 2
            for i in range(n)
            for j in range(n)
            if i != j
        )
        gaps.append(numerator / ((n - 1) * k * (k - 1) ** 3))
    gap_values = np.asarray(gaps, dtype=float)
    return {
        "scope": "Theorem 2 expected-advantage gap",
        "K_values": k_values.astype(int).tolist(),
        "exact_formula_values": gap_values.tolist(),
        "K_times_gap": (k_values * gap_values).tolist(),
        "loglog_slope": float(
            np.polyfit(np.log(k_values), np.log(gap_values), 1)[0]
        ),
        "certificate": (
            "numerator has degree 3 with positive leading coefficient and "
            "denominator has degree 4 with positive leading coefficient"
        ),
    }


def run_full() -> dict[str, object]:
    cases = [
        Case(seed=seed, k=k)
        for seed in FULL_SEEDS
        for k in (*PAPER_K, *EXTENDED_K)
    ]
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        rows = list(executor.map(run_case, cases))
    rows.sort(key=lambda row: (row["K"], row["seed"]))
    summary = full_summary(rows)
    required_values = [
        summary[k]["paper_compatibility"][metric][
            "within_empirical_predictive_interval95"
        ]
        for k in ("2", "4")
        for metric in ("mv", "isp")
    ]
    positive_paired_effects = [
        summary[k]["gap"]["mean_ci95_normal"][0] > 0
        for k in map(str, PAPER_K)
    ]
    compatible = all(required_values) and all(positive_paired_effects)
    return {
        "stage": "full",
        "verdict": "VERIFIED" if compatible else "BLOCKED",
        "assessment": (
            "paper K=2/K=4 values statistically compatible and paired ISP "
            "improvement positive across all paper K"
            if compatible
            else "pre-registered compatibility or paired-effect criterion failed"
        ),
        "N": 4,
        "M": M_QUESTIONS,
        "accuracies": ACCURACIES.tolist(),
        "paper_K": list(PAPER_K),
        "extended_K": list(EXTENDED_K),
        "seeds": list(FULL_SEEDS),
        "replicates": len(FULL_SEEDS),
        "configured_workers": WORKERS,
        "calibrated_from_pilot_replicates": 89,
        "rows": rows,
        "summary": summary,
        "accuracy_gap_scaling": accuracy_gap_scaling(rows),
        "expected_advantage_scaling": expected_advantage_scaling(),
        "acceptance": {
            "K2_K4_paper_values_within_predictive_interval95": all(
                required_values
            ),
            "paired_gap_mean_ci95_above_zero_all_paper_K": all(
                positive_paired_effects
            ),
        },
    }
