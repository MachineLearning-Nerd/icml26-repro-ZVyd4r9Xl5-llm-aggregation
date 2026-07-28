# Fixed command and compute

`uv run python repro/src/verify.py`

Estimated demand: one CPU core for Claim 6 itself, but the fixed cumulative
command reruns Claim 3 and therefore has uncertain runtime. The formal run uses
Hugging Face `cpu-upgrade` (8 allocated vCPU), while Claim 6 configures one
worker. Runtime is recorded from the formal run.
