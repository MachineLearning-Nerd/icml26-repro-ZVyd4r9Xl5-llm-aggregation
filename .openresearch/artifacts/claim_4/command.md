# Fixed command and compute

```text
uv run python repro/src/verify.py
```

Claim 4 configures one worker. The cumulative command also reruns Claim 3's
calibrated simulation, so estimated demand is 8 CPU cores and uncertain runtime
over five minutes before launch. It must run through Hugging Face
`cpu-upgrade`, whose documented allocation is 8 vCPU, 32 GB RAM, and 50 GB
disk. The environment is pinned by the repository-level `uv.lock`.
