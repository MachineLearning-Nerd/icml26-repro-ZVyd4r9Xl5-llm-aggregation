# Claim 3 source audit

Pinned source: <https://ar5iv.labs.arxiv.org/html/2510.01499>, retrieved
2026-07-28T17:44:20Z, SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

Section 5.1 (`#S5.SS1`) specifies `N=4`, accuracies
`0.6,0.7,0.8,0.9`, `M=10,000`, `K in {2,4,6,8,10}`, uniform random MV tie
breaking, and empirical second-order information estimated from the dataset.
Table 2 is `#S5.T2`; the extended gap figure is `#A5.F1`.

The paper gives no random seed. Therefore exact bit-for-bit recovery of one
stochastic table is not an honest contract. The final test will locate the
paper's reported values within a pre-calibrated distribution of faithful
single runs and will report the replicate mean separately.

The paper text informally connects the vanishing empirical accuracy gap to
Theorem 2. Theorem 2 is about expected advantage, not aggregation accuracy.
The final simulation will therefore label the accuracy-gap scaling as
empirical and will not use the theorem formula as its sample-size or slope
target.
