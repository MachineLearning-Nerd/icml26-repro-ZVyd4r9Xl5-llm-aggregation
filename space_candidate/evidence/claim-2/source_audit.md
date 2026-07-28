# Claim 2 source audit

Pinned source: <https://ar5iv.labs.arxiv.org/html/2510.01499>, retrieved
2026-07-28T17:44:20Z, SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

- Algorithm 2: `#alg2`
- Theorem 2: `#Thmtheorem2`
- Assumption 1: `#Thmassumption1`
- Section 4 chance premise: `#S4.p3`
- Appendix proof: `#A4.SS3`

The exact theorem is universal over the model parameters, not a statement
about one simulated accuracy vector. Section 4 adds the premise that every
agent is no worse than random guessing, `x_i >= 1/K`. This premise is
load-bearing because each displayed gap numerator contains
`(K*x_i-1)(K*x_j-1)^2`.

Algorithm 2 receives answers and the pairwise conditionals
`P(A_i=s | A_j=a)`. Ground-truth labels appear only in evaluation of the
expected advantage, not in aggregation.
