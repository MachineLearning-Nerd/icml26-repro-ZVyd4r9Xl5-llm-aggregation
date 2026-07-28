# Fixed command and compute

`uv run python repro/src/verify.py`

Estimated demand: one CPU core and less than five minutes, but runtime was
uncertain because the fixed command cumulatively reruns Claim 3. Per policy the
formal run uses Hugging Face `cpu-upgrade` (8 allocated vCPU); Claim 5 itself
configures one worker. Runtime is recorded from the formal run.
