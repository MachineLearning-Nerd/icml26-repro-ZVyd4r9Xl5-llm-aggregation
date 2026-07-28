# Claim 1 evaluation

Verdict: **VERIFIED**. Confidence: **HIGH**.

Formal OpenResearch run `e9b490a9-5453-44a9-894c-caca9e211f2a` executed commit
`058717d1224728e1aa64f2067eb3e6ecb266206b` under the fixed command.

- Universal symbolic likelihood-factorization certificate: PASS.
- Independent exact-rational checker: 418 complete answer profiles, zero
  OW/MAP argmax-set mismatches.
- Conditional-dependence negative control: PASS. With 70% marginal accuracy
  for all three agents, witness `(0,0,1)` gives `MAP=1` and `OW=0` after
  violating Assumption 1.
- Total HF job duration: 53 seconds. Claim verifier runtime: 0.128229 seconds.
- Flavor allocation: 8 vCPU and 32 GB (`cpu-upgrade`). The container's
  host-visible `os.cpu_count()` was 64 and is not treated as the allocation.

Raw evidence is in `raw/formal_result.json`,
`raw/independent_checker_output.json`, and
`raw/negative_control_output.json`. Any component failure makes the verifier
exit nonzero.
