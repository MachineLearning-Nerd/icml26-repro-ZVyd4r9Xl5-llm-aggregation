"""Independent slow implementation for one complete deterministic case."""

from __future__ import annotations

import hashlib
import json
from typing import Sequence

import numpy as np


ACCURACIES = (0.6, 0.7, 0.8, 0.9)


def digest_arrays(arrays: Sequence[np.ndarray]) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.dtype).encode())
        digest.update(str(contiguous.shape).encode())
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def main() -> int:
    seed, k, m = 19, 4, 256
    rng = np.random.default_rng(np.random.SeedSequence([seed, k, m]))
    truth = rng.integers(0, k, size=m)
    answers = np.empty((m, 4), dtype=np.int16)
    for i, accuracy in enumerate(ACCURACIES):
        correct = rng.random(m) < accuracy
        rank = rng.integers(0, k - 1, size=m)
        wrong = rank + (rank >= truth)
        answers[:, i] = np.where(correct, truth, wrong)

    pairwise = np.zeros((4, 4, k, k), dtype=float)
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            for label in range(k):
                for observed in range(k):
                    mask = answers[:, j] == observed
                    pairwise[i, j, label, observed] = (
                        np.mean(answers[mask, i] == label)
                        if np.any(mask)
                        else 1.0 / k
                    )

    count_scores = np.zeros((m, k), dtype=float)
    isp_scores = np.zeros((m, k), dtype=float)
    for question in range(m):
        for label in range(k):
            count_scores[question, label] = np.sum(answers[question] == label)
            predicted = 0.0
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    predicted += sum(
                        pairwise[i, j, label, alternative]
                        for alternative in range(k)
                        if alternative != answers[question, j]
                    ) / (k - 1)
            isp_scores[question, label] = (
                count_scores[question, label] - predicted / 3
            )

    tie_seed = (seed, k, m, 17)
    mv_rng = np.random.default_rng(np.random.SeedSequence(tie_seed))
    isp_rng = np.random.default_rng(np.random.SeedSequence(tie_seed))
    mv = np.asarray(
        [mv_rng.choice(np.flatnonzero(row == row.max())) for row in count_scores],
        dtype=np.int16,
    )
    isp = np.asarray(
        [isp_rng.choice(np.flatnonzero(row == row.max())) for row in isp_scores],
        dtype=np.int16,
    )
    output = {
        "status": "PASS",
        "imports_production_aggregation": False,
        "seed": seed,
        "K": k,
        "M": m,
        "digest": digest_arrays([truth, answers, mv, isp]),
        "mv_accuracy": float(np.mean(mv == truth)),
        "isp_accuracy": float(np.mean(isp == truth)),
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
