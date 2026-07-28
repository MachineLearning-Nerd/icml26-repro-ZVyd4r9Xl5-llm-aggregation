# Claim 2 — ISP dominates MV, which dominates SP

**Reviewer verdict: VERIFIED. Confidence: HIGH.**

## Exact claim and source

[Algorithm 2](https://ar5iv.labs.arxiv.org/html/2510.01499#alg2) computes ISP
from answers and the second-order conditionals `P(A_i=s | A_j=a)`, without
ground-truth labels.
[Theorem 2](https://ar5iv.labs.arxiv.org/html/2510.01499#Thmtheorem2) states

`E[Adv_ISP(s*)] >= E[Adv_MV(s*)] >= E[Adv_SP(s*)]`.

The source HTML was retrieved on 2026-07-28T17:44:20Z with SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.
The certified domain is every `N>=2`, every `K>=2`, and every
`x_i in [1/K,1]`. The premises are the uniform post-shuffle prior, uniform
errors over wrong labels, conditional independence given truth, exact
pairwise conditionals, and Section 4's explicit no-worse-than-random premise.

## Universal certificate

The verifier reconstructs the same-answer and different-answer conditionals
as exact sparse rational polynomials in symbolic `K,x,y`. Clearing
denominators proves both generic pairwise identities. Summing over ordered
pairs gives exactly

`E[Adv_ISP-Adv_MV]`

`= sum_(i!=j) (K*x_i-1)(K*x_j-1)^2 / ((N-1)K(K-1)^3)`

and

`E[Adv_MV-Adv_SP]`

`= sum_(i!=j) (K*x_i-1)(K*x_j-1)^2 / ((N-1)K(K-1)^2)`.

Every numerator term is nonnegative under `x_i>=1/K`; both denominators are
positive. This proves the ordering throughout the stated domain. The
Algorithm 2 function signature is exactly `answers, k, pairwise, variant`;
the production aggregator receives no truth labels.

## Formal and independent results

Formal run `c0cc58c9-cd23-411a-8484-e97dab92fed2`, Git SHA
`389613ee48ec988d25c64b66a91349ba5e89e386`.

| Check | Result |
| --- | --- |
| Generic ISP−MV identity | PASS |
| Generic MV−SP identity | PASS |
| Algorithm 2 label-interface audit | PASS: no truth input |
| Independent exact checker | PASS: 55 profiles |
| Scope negative control | PASS: both inequalities reversed |

The independent checker imports no production aggregation code and integrates
over every truth and answer profile with `fractions.Fraction`.

| K | N | Accuracies | Profiles | E[ISP] | E[MV] | E[SP] | Exact formulas |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| 2 | 2 | `1/2, 3/4` | 4 | `1/4` | `1/4` | `1/4` | PASS |
| 2 | 3 | `2/3, 3/4, 4/5` | 8 | `317/360` | `43/60` | `199/360` | PASS |
| 3 | 3 | `1/3, 1/2, 4/5` | 27 | `3173/4800` | `19/30` | `1387/2400` | PASS |
| 4 | 2 | `1/4, 3/5` | 16 | `7/20` | `7/20` | `7/20` | PASS |

## Negative control

For `K=2`, `N=2`, and accuracies `(2/5,9/10)`, the shuffle symmetry,
uniform errors, and conditional independence still hold, but the first agent
violates `x_i>=1/K`. The exact checker obtains

`E[Adv_ISP]=63/250 < E[Adv_MV]=3/10 < E[Adv_SP]=87/250`.

This intended reversal shows that the chance premise is load-bearing. It is a
scope control, not a falsification of Theorem 2.

## Reproduce

```text
uv run python repro/src/verify.py
```

Python 3.12 and dependencies are pinned by the visible `uv.lock`. The formal
run used Hugging Face `cpu-upgrade` (8 allocated vCPU, 32 GB RAM) and
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Scientific demand was
estimated at one core; remote execution was selected because setup/runtime
was uncertain. Total runtime was 47 seconds, the Claim 2 verifier used
0.105355 seconds, and estimated cost was at most $0.0005. The verifier exits
nonzero if any certificate, checker, control, or cumulative regression fails.

## Downloadable evidence

- [Claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/claim_contract.json)
- [Formal raw JSON](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/formal_result.json)
- [Independent output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/independent_checker_output.json)
- [Control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/negative_control_output.json)
- [Verifier](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/verifier.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/independent_checker.py)
- [Negative control](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/negative_control.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-2/run_metadata.json)

## Limitations

The certificate concerns population pairwise conditionals, exactly as in
Theorem 2. Finite-sample estimation is a separate theorem. `N=1` is excluded
because Algorithm 2 divides by `N-1`. The enumeration corroborates the
generic proof; it is not used to infer universal validity.
