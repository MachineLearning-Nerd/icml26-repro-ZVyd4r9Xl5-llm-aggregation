# Claim 1 — Optimal Weight is Bayes-optimal

**Reviewer verdict: VERIFIED. Confidence: HIGH.**

## Exact claim and source

Algorithm 1 assigns agent `i`

`omega_i = sigma_K^{-1}(x_i) = log(x_i (K-1)/(1-x_i))`

and returns the label maximizing the sum of weights cast for that label.
[Theorem 1](https://ar5iv.labs.arxiv.org/html/2510.01499#Thmtheorem1)
states that, under
[Assumption 1](https://ar5iv.labs.arxiv.org/html/2510.01499#Thmassumption1),
this rule is Bayesian-optimal for any admissible post-shuffle distribution.
The source HTML was retrieved on 2026-07-28T17:44:20Z with SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

The certified domain is every integer `N >= 1`, every integer `K >= 2`, every
accuracy vector with `0 < x_i < 1`, and every answer profile, assuming a
uniform post-shuffle prior, uniform errors over wrong labels, and conditional
independence given the truth.

## Universal derivation

For candidate `s`, let `v_i(s)=1{a_i=s}`. The conditional likelihood is

`L_s = product_i x_i^v_i(s) ((1-x_i)/(K-1))^(1-v_i(s))`.

The proof certificate checks the per-agent identity

`x_i^v ((1-x_i)/(K-1))^(1-v)`

`= ((1-x_i)/(K-1)) (x_i(K-1)/(1-x_i))^v`.

Multiplying over agents leaves a positive factor independent of `s`. The
uniform prior is also independent of `s`; both cancel from the MAP ordering.
Taking the strictly increasing logarithm gives exactly Algorithm 1's score.
This is a universal symbolic argument, not an inference from simulations.

## Formal results

Formal run: `e9b490a9-5453-44a9-894c-caca9e211f2a` at Git SHA
`058717d1224728e1aa64f2067eb3e6ecb266206b`.

| Check | Raw result | Interpretation |
| --- | ---: | --- |
| Symbolic factorization certificate | PASS | OW and MAP have the same complete argmax set |
| Independent exact-rational checker | 418/418 profiles, 0 mismatches | Corroborates below-chance, chance, and above-chance regimes |
| Negative control | PASS | Breaking conditional independence produces the intended OW/MAP disagreement |

The independent checker does not import the production aggregation
implementation. Its five complete finite domains are:

| K | N | Accuracies | Profiles exhausted | Mismatches |
| ---: | ---: | --- | ---: | ---: |
| 2 | 1 | `1/3` | 2 | 0 |
| 2 | 3 | `2/3, 3/4, 4/5` | 8 | 0 |
| 3 | 3 | `1/5, 1/3, 3/4` | 27 | 0 |
| 4 | 4 | `1/5, 1/4, 3/5, 4/5` | 256 | 0 |
| 5 | 3 | `1/6, 1/5, 5/6` | 125 | 0 |

## Negative control

The control retains a uniform prior and 70% marginal accuracy for all three
agents but uses a conditionally dependent error distribution. For observed
answers `(0,0,1)`,

- `P(answers | truth=0) = 1/100`;
- `P(answers | truth=1) = 1/10`;
- Bayes/MAP returns `1`;
- OW, using the identical 70% marginal accuracies, returns the majority label
  `0`.

This expected disagreement shows why Assumption 1 is load-bearing. It is not a
falsification because the control intentionally violates that assumption.

## Reproduce

The fixed command for every experiment node is:

```text
uv run python repro/src/verify.py
```

Python 3.12 and all dependencies are pinned by the visible `uv.lock`. The
formal run used Hugging Face `cpu-upgrade` (8 allocated vCPU, 32 GB RAM) and
the image `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Estimated scientific
demand was one core; the remote flavor was selected because fresh setup time
was uncertain. Total job runtime was 53 seconds, the Claim 1 verifier used
0.128229 seconds, and approximate compute cost was at most $0.0005.

The verifier exits nonzero if the certificate, independent checker, or control
fails.

## Downloadable evidence

- [Exact claim contract](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/claim_contract.json)
- [Formal raw JSON](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/formal_result.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/independent_checker_output.json)
- [Negative-control output](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/negative_control_output.json)
- [Proof certificate](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/proof_certificate.json)
- [Verifier source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/verifier.py)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/independent_checker.py)
- [Negative-control source](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/negative_control.py)
- [Run metadata](https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/evidence/claim-1/run_metadata.json)

## Limitations

The certificate covers interior accuracies. At accuracy exactly zero or one,
finite log-weights diverge; the limiting Bayes rule is not certified here.
Ties are compared as complete maximizing sets rather than by a particular
random tie-breaker. The finite enumeration is corroboration only; the
posterior factorization is the proof-level evidence.
