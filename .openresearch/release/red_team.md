# Evaluator-blind pre-publication red team

## Scope

- Candidate source branch: `orx/release-metadata-and-evaluator-blind-audit`
- First audited Git SHA: `1ce2adfad61cfc33232aa2d7ff18b3cdf57926f9`
- Corrected Git SHA: `105c515534a88a3849f75f28f61eb12252bd1e7a`
- Corrected GitHub archive SHA-256:
  `be9da33cf31ae6ec87aee09e462779bbc71f11a797bbb988c4d376e54bf7e262`
- Audit date: 2026-07-28
- Allowed knowledge: the downloaded candidate and the evaluator rubric only.
- Canonical starting points: `README.md`, `logbook.json`, and `pages/index.md`.
- Complete opened-file ledger: `red_team_opened_files.txt`.

The reviewer was not told where claim evidence lived. It began at each canonical
entrypoint, followed the visible navigation to the current report and all six
claim pages, and then opened every downloadable evidence link exposed by those
pages. Unpublished OpenResearch logs, local paths, and repository-only context
were not used to fill gaps.

## Pass 1 — defect discovery

Pass 1 downloaded the candidate at
`1ce2adfad61cfc33232aa2d7ff18b3cdf57926f9`. Navigation exposed all six
contracts, inline results, code, raw data, checkers, controls, limitations,
commands, environment, SHA, seed, CPU, and runtime fields. Historical content
was reachable under the exact navigation label `Historical rejected baseline`.

Two executable-release defects were found:

1. all visible claim verifiers called `git rev-parse HEAD` unconditionally,
   although a Hugging Face snapshot has no `.git` directory;
2. the Claim 5 verifier and independent checker looked for the CSV in a
   repository-internal `raw/` subdirectory rather than at its evaluator-visible
   candidate location.

Both defects were treated as missing evidence. No release forecast or upload was
accepted at this point.

## Fix

The visible verifiers now use live Git metadata when available and otherwise
read the immutable scientific Git SHA from the adjacent `run_metadata.json`.
The visible Claim 5 programs now read
`evidence/claim-5/appendix_tables_4_6.csv`, matching the linked candidate tree.
The internal research verifier retains its internal `raw/` layout.

## Pass 2 — fresh corrected archive

Pass 2 downloaded a new, empty-directory archive at
`105c515534a88a3849f75f28f61eb12252bd1e7a`; it did not reuse the fixed
working tree. Results:

- 118 files in the pristine candidate;
- 56 unique downloadable evidence/code links opened;
- zero broken downloadable links;
- all 35 JSON evidence files and `logbook.json` parse;
- both CSV files are present and readable;
- all five SVG evidence figures pass `xmllint --noout`;
- Claims 1, 2, 5, and 6 standalone verifiers exit zero with `VERIFIED`;
- Claim 4 standalone verifier exits zero with audit status `PASS` and the
  scientific verdict remains `BLOCKED`;
- the light, independent Claim 3 `K=4, M=256` checker exits zero and reports
  digest
  `1b6a3cf798b3062851bd1a4be51fa37bc8eeb7d2265f44e841807302c4d890fd`;
- the full Claim 3 verifier was not rerun locally because it uses eight workers;
  it is covered by the fixed-command Hugging Face cumulative regression;
- all 13 paths from the judged Space revision remain present;
- the historical executive-summary page is byte-identical;
- ten historical static/content files are byte-identical; only `README.md`,
  `logbook.json`, and `pages/index.md` change to add current navigation.

Standalone verifier execution created seven ignored `.pyc` files inside the
temporary audit directory. The downloaded archive contains zero `.pyc` paths,
and the upload allowlist is built from tracked pristine files only.

## Blind reviewer conclusions

| Claim | Located current verifier? | Exact contract and assumptions visible? | Inline data and raw link? | Checker/control? | Conclusion |
| --- | --- | --- | --- | --- | --- |
| 1 | Yes | Yes | Yes | PASS/PASS | VERIFIED |
| 2 | Yes | Yes | Yes | PASS/PASS | VERIFIED |
| 3 | Yes | Yes | Yes | PASS/PASS | VERIFIED; full regeneration delegated to the fixed HF regression |
| 4 | Yes | Yes | Yes | PASS/PASS | BLOCKED after four routes; no invalid falsification |
| 5 | Yes | Yes | Yes, all 48 rows | PASS/PASS | VERIFIED |
| 6 | Yes | Yes | Yes | PASS/PASS | VERIFIED |

No inaccessible conclusion remained after Pass 2. Claim 4 is not an
accessibility defect: the canonical page directly exposes why the exact finite
experiment is scientifically blocked and what would unblock it.
