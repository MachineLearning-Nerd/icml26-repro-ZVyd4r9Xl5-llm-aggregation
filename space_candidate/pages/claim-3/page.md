# Claim 3 — full `N=4, M=10,000` simulation

**Reviewer verdict: VERIFIED. Confidence: HIGH.**

## Headline evidence

The paper reports one stochastic run. Its seed is not disclosed, so the
faithful contract is whether those numbers are plausible single-run outcomes
under the exact setup—not whether an arbitrary new seed reproduces the same
last digits. A pre-run 8-seed pilot fixed 89 fresh full-run replicates.

| K | Method | Paper | 89-run mean | Mean 95% CI | Single-run predictive 95% | Paper z-score |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 2 | MV | 85.13% | 85.002% | 84.925–85.079% | 84.336–85.732% | 0.347 |
| 2 | ISP | 90.48% | 90.162% | 90.097–90.226% | 89.620–90.784% | 1.024 |
| 4 | MV | 92.64% | 92.378% | 92.319–92.436% | 91.860–92.914% | 0.929 |
| 4 | ISP | 94.45% | 94.414% | 94.366–94.463% | 93.966–94.828% | 0.154 |

All four paper values lie inside the pre-registered empirical 95% predictive
intervals. Every paper-grid paired ISP−MV mean CI is above zero.

## Exact source contract

[Section 5.1](https://ar5iv.labs.arxiv.org/html/2510.01499#S5.SS1)
and [Table 2](https://ar5iv.labs.arxiv.org/html/2510.01499#S5.T2)
specify:

- `N=4`, accuracies `(0.6,0.7,0.8,0.9)`;
- `M=10,000` questions per run;
- `K in {2,4,6,8,10}`;
- empirical pairwise conditionals estimated on those questions;
- uniformly random MV tie breaking.

The source HTML was retrieved on 2026-07-28T17:44:20Z with SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.
No question count, model count, or accuracy was downscaled.

## All paper-grid results

| K | Paper MV | Mean MV | Paper ISP | Mean ISP | Mean ISP−MV | Gap mean 95% CI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 85.13% | 85.002% | 90.48% | 90.162% | 5.160% | 5.095–5.225% |
| 4 | 92.64% | 92.378% | 94.45% | 94.414% | 2.037% | 1.992–2.081% |
| 6 | 94.22% | 94.057% | 95.78% | 95.610% | 1.554% | positive |
| 8 | 94.85% | 94.753% | 96.23% | 96.094% | 1.341% | positive |
| 10 | 95.54% | 95.200% | 96.49% | 96.392% | 1.193% | positive |

The full raw CSV contains 801 rows: 89 fresh seeds times the five paper and
four extended `K` values.

## Scaling audit

The finite paper grid gives mean accuracy gaps
`[0.05160, 0.02037, 0.01554, 0.01341, 0.01193]` and a log-log slope of
`-0.9016`. Across the 89 seed-wise slopes, the median is `-0.9155` and the
empirical 95% interval is `[-1.0212,-0.7517]`.

The paper's exact `Theta(1/K)` statement is about expected advantage, not
aggregation accuracy. Applying Theorem 2's exact formula on the independently
chosen grid `K={16,32,64,128,256,512}` gives slope `-0.9830`; `K*gap`
stabilizes from `1.591` to `1.697`. The polynomial certificate has a
positive degree-3 numerator and positive degree-4 denominator, which supplies
the proof-level asymptotic result. The accuracy slope remains finite-grid
empirical evidence only.

## Independent checker and controls

An independent slow implementation imports no production aggregation code and
matches the complete production digest for a deterministic 256-question case.

| Test | Result |
| --- | --- |
| Independent full-case digest | PASS: exact match |
| Uniform pairwise information | PASS: ISP and MV differ on 0/512 predictions |
| Sign-corrupted ISP mutation | PASS: rejected; 38/512 predictions differ |
| Claims 1–2 regression | PASS |

The sign mutation is a genuine negative control: replacing the ISP subtraction
with addition produces a distinct digest
`11447b8d...f4cf125` instead of `2fd3c14a...878696`.

## Reproduce

```text
uv run python repro/src/verify.py
```

The full run used seeds `1000..1088` and exactly 8 worker processes on Hugging
Face `cpu-upgrade` (8 allocated vCPU, 32 GB RAM), image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Estimated demand was 8 cores.
Total runtime was 74 seconds; the Claim 3 verifier used 30.777710 seconds;
estimated cost was at most $0.001. Python and dependencies are pinned in the
visible `uv.lock`. Any acceptance, digest, control, or cumulative-regression
failure exits nonzero.

## Downloadable evidence

- [Claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/claim_contract.json)
- [801-case raw CSV](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/replicates.csv)
- [Summary JSON](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/summary.json)
- [Independent output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/independent_checker_output.json)
- [Control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/negative_control_output.json)
- [Verifier](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/verifier.py)
- [Simulation and control source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/repro/claims/claim3_simulation.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/independent_checker.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-3/run_metadata.json)

## Limitations

The undisclosed author seed prevents bit-for-bit recovery of the single paper
run. The evidence instead establishes statistical compatibility under the
exact stated process. Pairwise conditionals are estimated and evaluated on
the same questions, matching the paper; this is not held-out generalization.
