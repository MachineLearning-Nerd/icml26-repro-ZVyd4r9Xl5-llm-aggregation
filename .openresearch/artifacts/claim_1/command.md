# Exact command and environment

Fixed OpenResearch command:

```text
uv run python repro/src/verify.py
```

The environment is Python 3.12 with the repository's committed `uv.lock`.
Hugging Face executions use
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim` on `cpu-upgrade`. The run log
prints the exact Git SHA, visible CPU count, Python version, and verifier
runtime. No environment variable changes claim behavior.
