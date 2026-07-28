# Command ledger

This ledger records every evidence-affecting or release-affecting command class
used in the campaign. Repeated read-only inspections (`git status`,
`git rev-parse`, `find`, `rg`, `sed`, `jq`, `shasum`, `cmp`, `comm`, `file`,
`df`, and `xmllint`) are listed once with their exact forms and inputs; they did
not mutate evidence.

## Orientation and immutable-source capture

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx skill orx-lit
orx skill orx-reports
orx projects --json
orx runs cbb4a316-4523-447c-9a95-11a79d0d9206
orx project view cbb4a316-4523-447c-9a95-11a79d0d9206
git branch -a
git status --short
git rev-parse HEAD
git rev-parse master
git ls-remote origin
df -h .
env | sed 's/=.*//' | sort
curl -fsSL -A 'OpenResearch-Reproduction/1.0 (contact: local-agent)' https://ar5iv.labs.arxiv.org/html/2510.01499
curl -fsSL -A 'OpenResearch-Reproduction/1.0 (contact: local-agent)' https://export.arxiv.org/e-print/2510.01499
orx paper 2510.01499 --full
```

The paper HTML SHA-256 is
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`;
the arXiv source archive SHA-256 is
`32d901cbb84cc5c1a89be6f183d6fa4f7685aeda9af0d79ce34a489b10fb9e99`.
The live verdict retrieval was filtered on the exact value
`space_id == "DineshAI/ZVyd4r9Xl5"`.

The protected Space was retrieved at the exact revision:

```text
git clone https://huggingface.co/spaces/DineshAI/ZVyd4r9Xl5
git checkout d6708e1563a1a80106e7be65e607f333e61ff023
find . -type f
shasum -a 256 <each protected file>
```

## Environment and fixed command

```text
uv lock
uv sync --locked
uv run python repro/src/verify.py
uv run marimo check --strict notebooks/llm_aggregation_tutorial.py
```

The fixed command above is the project command inherited by every experiment.
No experiment used an environment-prefixed behavioral knob.

## Experiment-tree creation

Each command used the project ID
`cbb4a316-4523-447c-9a95-11a79d0d9206`. The titles below are the exact node
titles. Every non-root command supplied its direct predecessor as `--parent`;
the durable tree, not this prose ledger, is authoritative for the UUID edge.

```text
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Baseline: judged reproduction with locked uv environment" --run-command "uv run python repro/src/verify.py"
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 1: universal OW Bayes proof certificate" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 1: evaluator-visible evidence milestone" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 2: universal ISP-MV-SP proof certificate" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 2: evaluator-visible exact evidence" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 3: calibrated simulation pilot" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 3: 89-replicate full simulation" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 3: evaluator-visible full evidence" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 5 exact 48-row ensemble aggregate" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 5 evaluator-visible exact evidence" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 6 Bradley-Terry inverse-logit certificate" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 6 evaluator-visible proof evidence" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 4 four-route real-data access audit" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Claim 4 evaluator-visible BLOCKED evidence" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Final report notebook and release gates" --parent <direct-parent-UUID>
orx create-experiment cbb4a316-4523-447c-9a95-11a79d0d9206 --title "Release metadata and evaluator-blind audit" --parent 6353f868-c6b5-4894-b454-5314c0eaa9e6
```

## Git mutation pattern

Each child was checked out, edited, staged, committed, and pushed before its
run. The repeated exact command pattern was:

```text
git fetch origin
git checkout <experiment branch>
git diff --check
git add <scoped changed paths>
git commit -m "<claim-specific summary>"
git push origin HEAD
git status --short
git rev-parse HEAD
```

No experiment branch was rebased or merged after a completed run. The baseline
root was frozen after its successful run.

## Formal runs

Every launch used this exact orchestration shape:

```text
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --timeout 600 --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait <experiment-id> --timeout 480
orx runs cbb4a316-4523-447c-9a95-11a79d0d9206
orx logs <run-id>
orx exp desc <experiment-id> --set "<evidence-backed result note>"
```

The resulting run IDs, in chronological order, are:

```text
ccd3bbe4-6b97-4764-8f2d-251ed41f472a
ccb52a9e-a6b7-41f8-a282-5f34cf02844f
e9b490a9-5453-44a9-894c-caca9e211f2a
36a20569-1487-467b-bb9b-abab054307fa
d5c31ebd-8a10-45b5-9ad9-20fd29ea2887
c0cc58c9-cd23-411a-8484-e97dab92fed2
bddcecbc-ed7c-413c-abe9-29ed40e1e7a2
c3a27694-2e24-4b4e-80f6-e40208f3244e
4f71ed53-a7aa-4871-999e-e98632b249cb
ee1eebf8-66c8-4692-96c4-086026423722
1250e06d-5c79-4505-8648-a8eef6f25179
6efd86d9-b710-41be-9d19-60423c21e602
496fdc10-90d8-438c-84e2-062cbf3da96e
7b2d02d1-507a-483f-8620-061e962dabca
6b93e113-6b33-46e3-9c5e-aa67665a5f53
2e4093b4-7d98-446d-9a8e-2b0892fea017
3a23c0a0-5be2-4ac4-821a-bfe7f1ccea51
```

## Evaluator-blind release checks

```text
curl -fsSL -A 'OpenResearch-Reproduction/1.0 (contact: local-agent)' -o candidate.tar.gz https://github.com/MachineLearning-Nerd/icml26-repro-ZVyd4r9Xl5-llm-aggregation/archive/<candidate-sha>.tar.gz
tar -xzf candidate.tar.gz
rg -o 'https://huggingface\.co/spaces/DineshAI/ZVyd4r9Xl5/resolve/main/[^)" ]+' README.md pages
find evidence -name '*.json' -print0 | xargs -0 -n1 jq empty
find pages -name '*.svg' -print0 | xargs -0 -n1 xmllint --noout
.venv/bin/python <fresh-candidate>/evidence/claim-1/verifier.py
.venv/bin/python <fresh-candidate>/evidence/claim-2/verifier.py
.venv/bin/python <fresh-candidate>/evidence/claim-3/independent_checker.py
.venv/bin/python <fresh-candidate>/evidence/claim-4/verifier.py
.venv/bin/python <fresh-candidate>/evidence/claim-5/verifier.py
.venv/bin/python <fresh-candidate>/evidence/claim-6/verifier.py
shasum -a 256 <every allowlisted file>
file -b <every allowlisted file>
cmp -s <judged path> <candidate path>
comm -23 <sorted judged paths> <sorted candidate paths>
rg -l 'hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' <every allowlisted file>
```

The secret-signature scan returned zero files. The exact 108-path payload is
in `upload_allowlist.txt`; its exact hashes are in `upload_manifest.sha256`.
