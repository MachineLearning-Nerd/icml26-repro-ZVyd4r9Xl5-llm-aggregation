# Claim 4 — exact Table 3 real-data result is BLOCKED

**Reviewer verdict: BLOCKED. Confidence: LOW.**

This is not a proxy reproduction. Exactly three materially different
verification routes remained unresolved, so a fourth route explicitly sought
a faithful falsification. It found no valid counterexample. The published
numbers are therefore neither VERIFIED nor FALSIFIED.

## Exact contract

Section 5.4 and [Table 3](https://ar5iv.labs.arxiv.org/html/2510.01499#S5.T3)
report the strongest four-model ensemble:

`GPT-4o-2024-11-20 + Qwen2.5-Instruct-14B + Llama3.1-8B-Instruct + Phi-4`.

| Dataset | Retained examples | K | Paper OW-L | Paper MV | Reported lift |
| --- | ---: | ---: | ---: | ---: | ---: |
| UltraFeedback | 56,380 | 2 | 73.66% | 72.21% | +1.45 pp |
| MMLU | 109,820 | 4 | 90.37% | 89.32% | +1.05 pp |
| ARMMAN | 11,785 | 2 | 85.78% | 85.24% | +0.54 pp |

Verification requires the exact retained rows, labels and shuffle maps; the
four named models and inference settings; per-example predictions; and an
independently checked OW-L implementation. A falsification must contradict the
same finite experimental object. A different stochastic GPT sample, model,
dataset subset, or optimizer is not a contradiction.

The source HTML was retrieved with an explicit User-Agent at
2026-07-28T17:44:20Z, SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.
The source archive was independently retrieved at 2026-07-28T19:02:00Z,
SHA-256
`32d901cbb84cc5c1a89be6f183d6fa4f7685aeda9af0d79ce34a489b10fb9e99`.

## Four verification-oriented routes

| Route | Defensible interpretation | Method | Result | Control |
| --- | --- | --- | --- | --- |
| 1 — release discovery | An author cache and code can substitute for regenerating inference | Search arXiv source, GitHub repository metadata, and HF dataset metadata by exact title, arXiv ID, and ISP name | No code or prediction cache found; archive contains TeX, two figures, and styles | Same HF search located public UltraFeedback and MMLU |
| 2 — faithful regeneration | Recreate exact model outputs from documented setup | Audit every row, shuffle, model, inference, data, and implementation dependency | Exact retained IDs/shuffles absent; ARMMAN records absent; Azure deployment/provenance absent; paper OW-L code absent; open models were run on disallowed A100 GPU | Public bases found for UltraFeedback/MMLU, none for ARMMAN records |
| 3 — aggregate reconstruction | Table 3 plus sample sizes might identify the raw result | Independently enumerate integer counts that round to all six cells | Five of six cells have 2–11 possible counts; no cell identifies row-level joint predictions needed by OW-L | One-hundredth mutation is rejected |
| 4 — mandatory falsification | Seek a contradiction under the exact finite configuration | Reject any counterexample that changes rows, models, stochastic outputs, prompts, shuffles, or OW-L | No assumption-matching counterexample can be constructed from aggregates | Table-only pseudo-evidence is rejected |

The full interpretations, commands, results, and controls are in the
[route record](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/route_evidence.json).

## Independent count audit

The checker uses only integer enumeration and `Decimal`, and imports no
production aggregation code.

| Dataset | Method | Candidate correct counts consistent with displayed percent |
| --- | --- | --- |
| UltraFeedback | OW-L | 41,527–41,532 (6 possibilities) |
| UltraFeedback | MV | 40,710–40,714 (5) |
| MMLU | OW-L | 99,239–99,249 (11) |
| MMLU | MV | 98,086–98,096 (11) |
| ARMMAN | OW-L | 10,109 (1) |
| ARMMAN | MV | 10,045–10,046 (2) |

Even the unique ARMMAN OW-L count does not say which examples were correct or
what any of four models predicted. OW-L is learned from pairwise prediction
correlations; method-level accuracy counts cannot reconstruct those inputs.

## Missing capabilities

| Required capability | Available? |
| --- | --- |
| Exact retained row IDs | No |
| Exact shuffle maps | No |
| Exact strong-model predictions | No |
| ARMMAN health/call records and labels | No |
| Exact Azure deployment and stochastic provenance | No |
| Paper's executable OW-L implementation | No |

The paper says GPT was accessed through Microsoft Azure at temperature 1.0
and top-p 1.0. The open models were generated through vLLM on one A100 with
default seed 0. This campaign is CPU-only and cannot use that hardware. More
importantly, substituting a new stochastic run would not recover the reported
finite predictions.

## Formal audit and negative control

```text
uv run python repro/src/verify.py
```

The fixed cumulative command emitted:

```text
CLAIM_4_RESULT={"audit_status":"PASS","verdict":"BLOCKED",
 "faithful_rerun_not_ready":true,
 "table_only_bundle_rejected":true,
 "four_materially_distinct_methods":true}
CUMULATIVE_VERDICT claim_4=BLOCKED
```

`audit_status=PASS` means the BLOCKED assessment is complete and internally
consistent. It does **not** mean Table 3 was reproduced.

Run `6b93e113-6b33-46e3-9c5e-aa67665a5f53`, Git SHA
`75d54637917cc31e247149c389154b73f13272af`, completed in 90 seconds on HF
`cpu-upgrade`. Estimated demand was 8 cores because the fixed command reruns
Claim 3; documented allocation was 8 vCPU and 32 GB RAM. Claim 4 itself used
one worker for 0.669371 seconds. Estimated cost was at most $0.001.

## Downloadable evidence and executable code

- [Claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/claim_contract.json)
- [Four-route record](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/route_evidence.json)
- [Public discovery output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/public_discovery.json)
- [Published Table 3 data](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/published_table3.json)
- [Formal output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/formal_result.json)
- [Independent output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/independent_checker_output.json)
- [Negative-control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/negative_control_output.json)
- [Verifier](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/verifier.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/independent_checker.py)
- [Contract implementation](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/repro/claims/claim4_real_data.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/run_metadata.json)
- [Limitations](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-4/limitations.md)

## Concrete unblocker

Release the exact retained row IDs, shuffle maps, per-example predictions for
the four strong models, ARMMAN records and labels under an appropriate
data-use agreement, OW-L implementation, and stochastic inference provenance;
or release an author-generated prediction cache plus code sufficient to
regenerate Table 3.
