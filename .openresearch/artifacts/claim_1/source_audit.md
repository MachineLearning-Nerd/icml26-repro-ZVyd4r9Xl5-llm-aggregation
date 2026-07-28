# Claim 1 source audit

Source: ar5iv HTML for arXiv 2510.01499, retrieved with explicit User-Agent on
2026-07-28T17:44:20Z.

- URL: <https://ar5iv.labs.arxiv.org/html/2510.01499>
- SHA-256: `f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`
- Model and shuffle properties: Proposition 1 and Assumption 1 in Section 2,
  anchors `#Thmproposition1` and `#Thmassumption1`.
- Weight formula and decision rule: Section 3 paragraph `#S3.p1` and Algorithm
  1 at `#alg1`.
- Exact theorem: Theorem 1 at `#Thmtheorem1`.

The theorem says that, under conditional independence, Algorithm 1 is the
Bayesian-optimal aggregator for any admissible post-shuffle distribution. The
paper defines Bayesian optimality over all aggregation algorithms, not only
linear rules, by maximizing the posterior probability of the correct label.

The source uses `K` (uppercase), not the judge text's lowercase `k`. The
quantifier “for any P” is conditional on the post-shuffle structural properties
and Assumption 1. Boundary accuracies zero and one make the displayed finite
inverse link diverge; this verifier proves the theorem on the explicit interior
domain `0 < x_i < 1` and records the boundary as a limitation.
