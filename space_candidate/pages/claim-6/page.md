# Claim 6 — binary OW weights are Bradley–Terry logits

**Reviewer verdict: VERIFIED. Confidence: HIGH.**

## Headline evidence

For every finite-domain accuracy `x in (0,1)`, write `z=exp(w)>0`.
Inverting the binary OW link is a four-step identity:

```text
x = z/(1+z)
x(1+z) = z
z(1-x) = x
w = log(z) = log(x/(1-x))
```

Because `1-x>0` and the exponential is a bijection from the reals to the
positive reals, this solution exists and is unique. Thus Algorithm 1's binary
weight is exactly the log-odds, and therefore is also proportional to it under
any common positive rescaling.

The Bradley–Terry probability independently factors as:

```text
P(1 beats 0) = exp(r1)/(exp(r1)+exp(r0))
             = exp(r1-r0)/(1+exp(r1-r0))
             = sigmoid(r1-r0).
```

Therefore `r1-r0=log(p/(1-p))`: the same inverse logistic.

## Exact source and domain

[Corollary 1](https://ar5iv.labs.arxiv.org/html/2510.01499#Thmcorollary1)
states the binary proportionality, and
[Appendix C.2](https://ar5iv.labs.arxiv.org/html/2510.01499#A3.SS2)
derives it from Algorithm 1. The source HTML was retrieved
2026-07-28T17:44:20Z with SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

As a primary LLM cross-check, Ouyang et al.
[arXiv:2203.02155](https://arxiv.org/abs/2203.02155), Equation 1, uses
`log sigmoid(r(x,y_w)-r(x,y_l))` for its reward-model comparison loss.

The finite real identity is `0<x<1`. At `x=0` and `x=1`, the weights are
extended-real limits `-infinity` and `+infinity`. The corollary does not impose
Theorem 2's no-worse-than-random premise, so this certificate covers the whole
strict-interior probability domain.

## Numerical reconstruction

The BT scores use an arbitrary common offset of 7.25 to confirm offset
invariance.

| Accuracy x | logit(x) | sigmoid(logit) | BT probability | Maximum error |
| ---: | ---: | ---: | ---: | ---: |
| 0.001 | -6.906755 | 0.0010000000 | 0.0010000000 | 6.51e-19 |
| 0.1 | -2.197225 | 0.10000000 | 0.10000000 | 2.78e-17 |
| 0.5 | 0.000000 | 0.50000000 | 0.50000000 | 0.00e+0 |
| 0.6 | 0.405465 | 0.60000000 | 0.60000000 | 1.11e-16 |
| 0.75 | 1.098612 | 0.75000000 | 0.75000000 | 1.11e-16 |
| 0.9 | 2.197225 | 0.90000000 | 0.90000000 | 1.11e-16 |
| 0.999 | 6.906755 | 0.99900000 | 0.99900000 | 1.11e-16 |

The independent checker also proves exact rational composition for
`x in {1/1000,1/10,1/2,3/4,9/10,999/1000}` and uses a separate 60-digit
Decimal `ln`/`exp` route. Its largest numerical error is `4e-60`.

## Controls

| Test | Result |
| --- | --- |
| Substitute wrong transform log(x) at x=0.75 | PASS: rejected; sigmoid(log(.75)) = 0.428571 |
| Treat x=0 or x=1 as a finite logit | PASS: both rejected; limits recorded |
| Multiply all weights by +3 | PASS: argmax preserved |
| Multiply all weights by -3 | PASS: argmax reverses, so negative “proportionality” is rejected |
| Independent Fraction/Decimal checker | PASS |
| Claims 1–3 and 5 regression | PASS |

## Reproduce

```text
uv run python repro/src/verify.py
```

Formal run `496fdc10-90d8-438c-84e2-062cbf3da96e`, Git SHA
`94301164890bf3985097517e9e08b1aa46b22fc5`. Estimated demand was eight
cores because the fixed cumulative command reruns Claim 3. It ran on Hugging
Face `cpu-upgrade` (8 allocated vCPU, 32 GB RAM), image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Claim 6 configures one
worker and took 0.052072 seconds; total runtime was 79 seconds; estimated cost
was at most $0.001. The host exposed 64 logical CPUs, distinct from the
documented 8-vCPU allocation. The environment is pinned in visible `uv.lock`.

## Downloadable evidence

- [Claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/claim_contract.json)
- [Proof certificate](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/proof_certificate.json)
- [Formal output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/formal_result.json)
- [Independent output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/independent_checker_output.json)
- [Control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/negative_control_output.json)
- [Verifier](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/verifier.py)
- [Production identity source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/repro/claims/claim6_bt.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/independent_checker.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-6/run_metadata.json)

## Limitations

This establishes the algebraic connection. It does not claim that arbitrary
real LLM preference data satisfy the Bradley–Terry model. BT score offsets are
unidentifiable, and a common positive scale acts as a temperature. Perfect
accuracy has an infinite, not finite, logit.
