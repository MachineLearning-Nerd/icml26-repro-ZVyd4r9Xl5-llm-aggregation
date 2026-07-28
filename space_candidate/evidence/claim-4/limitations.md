# Limitations and deviations

- No raw real-world model prediction was available or generated.
- No ARMMAN patient/call record was accessed.
- No Azure or other model API was called.
- No GPU was used; substituting CPU inference for the paper's A100/vLLM setup
  would not reproduce its exact stochastic predictions.
- The Table 3 arithmetic is source validation, not experimental verification.
- Public metadata search is time-bounded and cannot prove that an undiscovered
  private or newly released artifact does not exist.

Verdict: **BLOCKED**, not VERIFIED or FALSIFIED.
