# Claim 6 source audit

Corollary 1 (`#Thmcorollary1`) states the binary proportional inverse-logistic
weight. Appendix C.2 (`#A3.SS2`) says Algorithm 1 gives
`omega_i = sigma_2^{-1}(x_i)` and identifies `sigma_2` with the logistic
function. The source HTML was retrieved 2026-07-28T17:44:20Z and has SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.

The paper's cited LLM application, Ouyang et al. arXiv:2203.02155 Equation 1,
uses `log sigma(r(x,y_w)-r(x,y_l))` in its reward-model loss. This independently
anchors the Bradley-Terry logistic score-difference convention.

The finite inverse is defined for `0 < x < 1`. At `x=0` and `x=1`, the extended
limits are negative and positive infinity. The corollary itself does not impose
the no-worse-than-random premise used by Theorem 2, so the proof certificate
covers the complete strict-interior probability domain.
