# Claim 4 source audit

Claim 4 is a finite empirical report, not a universal theorem. Section 5.4 and
Table 3 (`#S5.SS4`, `#S5.T3`) select the strongest model from each of four
families: GPT-4o-2024-11-20, Qwen2.5-Instruct-14B,
Llama3.1-8B-Instruct, and Phi-4. The six exact reported percentages are stored
in `published_table3.json`.

Appendix E.3 (`#A5.SS3`) specifies 56,380 retained UltraFeedback examples,
109,820 successfully answered MMLU examples, and 11,785 successfully answered
ARMMAN cases. It says GPT models were accessed through Microsoft Azure with
temperature 1.0 and top-p 1.0. Open models were generated through vLLM on one
A100 with default seed 0. It does not identify the retained row IDs, shuffle
maps, Azure deployment or seed, per-example predictions, or executable OW-L
implementation. ARMMAN inputs contain health information and call records for
12,000 women and were obtained through a nonprofit collaboration.

The HTML was retrieved with an explicit User-Agent at
2026-07-28T17:44:20Z, SHA-256
`f9f8bd43851f5d7c44cc21550d2ee2a85bf2bdf20f94b0fdb2a50a76d1406fd0`.
The arXiv source archive was retrieved with an explicit User-Agent at
2026-07-28T19:02:00Z, SHA-256
`32d901cbb84cc5c1a89be6f183d6fa4f7685aeda9af0d79ce34a489b10fb9e99`.

The claim is verified only by regenerating the point estimates from faithful
raw predictions. Reprinting or arithmetically checking Table 3 is not
verification. A falsification must use the same finite experimental object;
different stochastic outputs or substitute datasets/models do not contradict
the reported run.
