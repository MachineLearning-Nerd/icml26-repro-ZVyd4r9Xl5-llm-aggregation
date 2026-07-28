# Claim 3 limitations

The reported paper table is one stochastic realization with no disclosed
seed. The 89-replicate result assesses statistical compatibility but cannot
prove that it recovered the authors' exact RNG stream.

An empirical finite-K accuracy slope does not prove an asymptotic Theta claim.
The report distinguishes the observed `K=2..10` accuracy-gap slope from Claim
2's exact expected-advantage formula. The latter supplies the proof-level
Theta evidence.

The pairwise conditionals are estimated and evaluated on the same 10,000
questions, matching the paper's stated protocol. This is not a held-out
generalization study.
