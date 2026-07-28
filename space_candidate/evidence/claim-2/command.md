# Reproduction command

Every experiment node inherits the same command:

```text
uv run python repro/src/verify.py
```

Python and dependencies are pinned by the repository-level `.python-version`,
`pyproject.toml`, and `uv.lock`.
