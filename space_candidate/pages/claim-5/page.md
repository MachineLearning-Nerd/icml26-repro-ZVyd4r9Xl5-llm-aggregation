# Claim 5 — exact 48-case ensemble aggregate

**Reviewer verdict: VERIFIED. Confidence: HIGH.**

## Headline evidence

The complete Appendix E.4 design has 16 one-model-per-family ensembles on
each of three datasets: 48 dataset–ensemble cases. Exact recomputation gives:

| Quantity | Recomputed result | Paper statement |
| --- | ---: | ---: |
| OW-L strictly beats MV | 47/48 = **97.92%** | 97.92% |
| UltraFeedback OW-L wins | 16/16 | — |
| MMLU OW-L wins | 16/16 | — |
| ARMMAN OW-L wins | 15/16 | — |
| Best proposed method lift over MV | **0.54–14.20 pp** | 0.54–14.20 pp |

## Exact quantifier guard

These are two related but different summaries. The 97.92% count compares
**OW-L** with MV. The 0.54–14.20 range is
`max(OW-L, OW-I, ISP) − MV` in every row, matching the source sentence that
MV is never best. OW-L alone has signed changes from **−0.51 to +14.20
percentage points** (and its smallest positive lift is 0.04), so the common
OW-L-only reading of the 0.54 minimum is explicitly rejected.

Source: [Section 5.4](https://ar5iv.labs.arxiv.org/html/2510.01499#S5.SS4.p3)
and [Tables 4–6](https://ar5iv.labs.arxiv.org/html/2510.01499#A5.SS4).
The HTML was retrieved 2026-07-28T17:44:20Z with SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

## All 48 published rows

`Best lift` is `max(OW-L, OW-I, ISP) − MV`, in percentage points.

| Dataset | Ensemble | OW-L | OW-I | ISP | MV | Best lift |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| UltraFeedback | GS, QS, LS, PS | 73.66 | 73.66 | 73.26 | 72.21 | 1.45 |
| UltraFeedback | GS, QS, LS, PW | 72.64 | 72.64 | 72.09 | 69.89 | 2.75 |
| UltraFeedback | GW, QS, LS, PS | 70.88 | 71.15 | 70.78 | 68.01 | 3.14 |
| UltraFeedback | GW, QS, LS, PW | 69.00 | 69.00 | 67.73 | 65.11 | 3.89 |
| UltraFeedback | GS, QS, LW, PS | 73.66 | 73.66 | 73.18 | 72.11 | 1.55 |
| UltraFeedback | GS, QS, LW, PW | 72.64 | 72.64 | 71.57 | 69.23 | 3.41 |
| UltraFeedback | GW, QS, LW, PS | 71.15 | 71.15 | 70.46 | 67.20 | 3.95 |
| UltraFeedback | GW, QS, LW, PW | 67.10 | 67.10 | 66.77 | 64.18 | 2.92 |
| UltraFeedback | GS, QW, LS, PS | 71.19 | 71.19 | 71.74 | 71.15 | 0.59 |
| UltraFeedback | GS, QW, LS, PW | 69.17 | 69.17 | 68.66 | 67.81 | 1.36 |
| UltraFeedback | GW, QW, LS, PS | 69.87 | 69.87 | 67.97 | 66.09 | 3.78 |
| UltraFeedback | GW, QW, LS, PW | 63.08 | 63.08 | 63.90 | 62.84 | 1.06 |
| UltraFeedback | GS, QW, LW, PS | 72.78 | 72.78 | 70.17 | 70.23 | 2.55 |
| UltraFeedback | GS, QW, LW, PW | 69.17 | 69.17 | 67.30 | 66.59 | 2.58 |
| UltraFeedback | GW, QW, LW, PS | 68.33 | 68.33 | 66.45 | 64.75 | 3.58 |
| UltraFeedback | GW, QW, LW, PW | 63.32 | 63.32 | 62.41 | 61.07 | 2.25 |
| MMLU | GS, QS, LS, PS | 90.37 | 90.37 | 90.01 | 89.32 | 1.05 |
| MMLU | GS, QS, LS, PW | 89.59 | 89.74 | 89.26 | 87.09 | 2.65 |
| MMLU | GW, QS, LS, PS | 87.62 | 87.57 | 87.08 | 86.06 | 1.56 |
| MMLU | GW, QS, LS, PW | 85.36 | 85.36 | 83.33 | 82.60 | 2.76 |
| MMLU | GS, QS, LW, PS | 90.42 | 90.51 | 90.20 | 89.57 | 0.94 |
| MMLU | GS, QS, LW, PW | 89.63 | 89.61 | 88.99 | 86.82 | 2.81 |
| MMLU | GW, QS, LW, PS | 87.90 | 87.91 | 87.23 | 86.01 | 1.90 |
| MMLU | GW, QS, LW, PW | 84.72 | 84.75 | 82.88 | 81.38 | 3.37 |
| MMLU | GS, QW, LS, PS | 89.03 | 89.03 | 88.57 | 87.49 | 1.54 |
| MMLU | GS, QW, LS, PW | 87.27 | 87.27 | 85.14 | 84.26 | 3.01 |
| MMLU | GW, QW, LS, PS | 84.58 | 84.58 | 83.92 | 83.57 | 1.01 |
| MMLU | GW, QW, LS, PW | 80.82 | 80.77 | 80.45 | 79.98 | 0.84 |
| MMLU | GS, QW, LW, PS | 89.35 | 89.38 | 88.64 | 87.55 | 1.83 |
| MMLU | GS, QW, LW, PW | 86.73 | 86.77 | 84.75 | 83.26 | 3.51 |
| MMLU | GW, QW, LW, PS | 84.49 | 84.80 | 84.03 | 82.89 | 1.91 |
| MMLU | GW, QW, LW, PW | 80.10 | 80.39 | 79.40 | 78.18 | 2.21 |
| ARMMAN | GS, QS, LS, PS | 85.78 | 85.78 | 85.78 | 85.24 | 0.54 |
| ARMMAN | GS, QS, LS, PW | 85.38 | 85.35 | 85.35 | 83.41 | 1.97 |
| ARMMAN | GW, QS, LS, PS | 84.30 | 84.57 | 82.77 | 78.96 | 5.61 |
| ARMMAN | GW, QS, LS, PW | 77.92 | 81.04 | 79.50 | 75.74 | 5.30 |
| ARMMAN | GS, QS, LW, PS | 85.78 | 85.78 | 85.78 | 84.83 | 0.95 |
| ARMMAN | GS, QS, LW, PW | 85.35 | 85.35 | 85.35 | 82.55 | 2.80 |
| ARMMAN | GW, QS, LW, PS | 84.30 | 84.59 | 82.32 | 78.76 | 5.83 |
| ARMMAN | GW, QS, LW, PW | 74.48 | 77.46 | 77.37 | 74.99 | 2.47 |
| ARMMAN | GS, QW, LS, PS | 84.89 | 84.89 | 85.18 | 81.33 | 3.85 |
| ARMMAN | GS, QW, LS, PW | 85.32 | 81.16 | 80.64 | 78.08 | 7.24 |
| ARMMAN | GW, QW, LS, PS | 84.30 | 73.36 | 73.31 | 72.72 | 11.58 |
| ARMMAN | GW, QW, LS, PW | 74.48 | 68.85 | 68.82 | 69.06 | 5.42 |
| ARMMAN | GS, QW, LW, PS | 84.63 | 84.58 | 83.66 | 78.00 | 6.63 |
| ARMMAN | GS, QW, LW, PW | 85.32 | 79.75 | 80.06 | 74.73 | 10.59 |
| ARMMAN | GW, QW, LW, PS | 84.30 | 68.53 | 72.16 | 70.10 | 14.20 |
| ARMMAN | GW, QW, LW, PW | 74.48 | 74.48 | 67.06 | 65.35 | 9.13 |

Abbreviations: GS/GW are GPT-4o-2024-11-20/GPT-35-turbo-0125;
QS/QW are Qwen2.5-Instruct-14B/3B; LS/LW are
Llama3.1-8B-Instruct/Llama3.2-1B-Instruct; PS/PW are Phi-4/Phi-4-mini-instruct.

## Independent checker and negative controls

The production route uses exact decimal arithmetic and validates that every
dataset has the complete 2×2×2×2 Cartesian design. A separately written
checker imports no production module and converts every displayed percentage
to integer hundredths of a percentage point.

| Test | Result |
| --- | --- |
| Independent 48-row integer recomputation | PASS: 47 wins, min 54, max 1420 hundredths pp |
| Count mutation | PASS: rejected after reducing the count to 46 |
| Maximum-lift mutation | PASS: rejected after reducing the maximum to 11.58 pp |
| OW-L-only range conflation | PASS: rejected; actual signed range −0.51–14.20 pp |
| Claims 1–3 regression | PASS |

## Reproduce

```text
uv run python repro/src/verify.py
```

Formal run `1250e06d-5c79-4505-8648-a8eef6f25179`, Git SHA
`fdcb642148ffb3872e43ac2d5f013b5ef4c91d3a`. Estimated demand was eight
cores because the fixed cumulative command reruns Claim 3. It ran on Hugging
Face `cpu-upgrade` (8 allocated vCPU, 32 GB RAM), image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Claim 5 configures one
worker and took 0.055232 seconds; total runtime was 85 seconds; estimated cost
was at most $0.001. The host exposed 64 logical CPUs, but the documented flavor
allocation—not host visibility—is the allocation record. The environment is
pinned in visible `uv.lock`.

## Downloadable evidence

- [Claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/claim_contract.json)
- [All 48 source rows (CSV)](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/appendix_tables_4_6.csv)
- [Formal output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/formal_result.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/independent_checker_output.json)
- [Negative-control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/negative_control_output.json)
- [Verifier](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/verifier.py)
- [Production arithmetic source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/repro/claims/claim5_tables.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/independent_checker.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-5/run_metadata.json)

## Limitations

This exactly verifies the paper's aggregate arithmetic, ensemble composition,
and quantifiers from every displayed per-ensemble row. It does not regenerate
the unreleased LLM predictions. Claim 4 separately audits whether those raw
real-data accuracies can be reproduced.
