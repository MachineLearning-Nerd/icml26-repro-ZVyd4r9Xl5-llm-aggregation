# Reproducing “Beyond Majority Voting”

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/blob/master/notebooks/llm_aggregation_tutorial.py)

This repository reproduces the six judged claims of
*Beyond Majority Voting: LLM Aggregation by Leveraging Higher-Order
Information* (arXiv:2510.01499).

Five claims are **VERIFIED** with executable evidence: OW's Bayes-optimality,
the ISP ≥ MV ≥ SP ordering, the full N=4/M=10,000 simulation, the exact 47/48
ensemble aggregate, and the Bradley–Terry inverse-logit connection. The exact
real-data Table 3 run is honestly **BLOCKED** after four routes because its
prediction caches, ARMMAN records, shuffle maps, Azure provenance, and OW-L
implementation are unavailable.

The paper reports ISP/MV of 90.48/85.13% at K=2 and 94.45/92.64% at K=4.
Across 89 full-size seeds we observe mean ISP/MV of 90.16/85.00% and
94.41/92.38%; every paper value is inside the corresponding empirical
single-run 95% predictive range. Compute was CPU-only on Hugging Face
`cpu-upgrade` (8 allocated vCPU); no GPU or proxy real-data run was used.

- [Illustrated technical report](reports/llm-aggregation-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/llm_aggregation_tutorial.py)
- [Evaluator-visible Space candidate](space_candidate/pages/index.md)

## Experiment log

All experiment nodes inherit the exact command `uv run python repro/src/verify.py`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| [`orx/baseline-judged-reproduction-with-locked-uv-envi`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/baseline-judged-reproduction-with-locked-uv-envi) | Frozen baseline and uv lock | `uv run python repro/src/verify.py` | Baseline complete | HF cpu-upgrade, 42 s successful |
| [`orx/claim-1-universal-ow-bayes-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-1-universal-ow-bayes-proof-certificate) | Universal OW/MAP certificate | `uv run python repro/src/verify.py` | VERIFIED | HF cpu-upgrade, 53 s |
| [`orx/claim-2-universal-isp-mv-sp-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-2-universal-isp-mv-sp-proof-certificate) | Exact advantage ordering | `uv run python repro/src/verify.py` | VERIFIED | HF cpu-upgrade, 47 s |
| [`orx/claim-3-89-replicate-full-simulation`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-3-89-replicate-full-simulation) | 89-seed full simulation | `uv run python repro/src/verify.py` | VERIFIED | HF cpu-upgrade, 74 s |
| [`orx/claim-5-exact-48-row-ensemble-aggregate`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-5-exact-48-row-ensemble-aggregate) | Exact Appendix table audit | `uv run python repro/src/verify.py` | VERIFIED | HF cpu-upgrade, 85 s |
| [`orx/claim-6-bradley-terry-inverse-logit-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-6-bradley-terry-inverse-logit-certificate) | Universal BT/logit proof | `uv run python repro/src/verify.py` | VERIFIED | HF cpu-upgrade, 79 s |
| [`orx/claim-4-four-route-real-data-access-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/claim-4-four-route-real-data-access-audit) | Three verification routes + mandatory falsification | `uv run python repro/src/verify.py` | BLOCKED | HF cpu-upgrade, 90 s |
| [`orx/final-report-notebook-and-release-gates`](https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/tree/orx/final-report-notebook-and-release-gates) | Cumulative release regression | `uv run python repro/src/verify.py` | 5 VERIFIED, 1 BLOCKED | HF cpu-upgrade, 95 s |
| `master` | Publication surface | Not run as an experiment (publication surface) | Reader-facing mirror | No experiment compute |

## Reproduce

```bash
uv sync --frozen
uv run python repro/src/verify.py
```

The environment is pinned to Python 3.12 in `uv.lock`. The cumulative command
is CPU-intensive because Claim 3 runs 801 full-size simulations; use the
documented OpenResearch/HF compute path rather than an interactive laptop.

For the tutorial:

```bash
uv run marimo edit notebooks/llm_aggregation_tutorial.py
uv run marimo run notebooks/llm_aggregation_tutorial.py
```
