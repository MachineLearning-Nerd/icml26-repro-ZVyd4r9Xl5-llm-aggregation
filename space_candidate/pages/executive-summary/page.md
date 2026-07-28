# Executive Summary


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1ec876065eef", "created_at": "2026-07-28T09:12:42+00:00", "title": "Verdict: 5/6 verified (10 pts)"}
-->
**Paper:** Optimal Weighted (OW) aggregation of LLM ensembles; ISP/MV/SP dominance (arXiv 2510.01499).

**Method:** Clean-room closed-form optimal weights (Bradley-Terry logit weights), ISP-dominance, and ensemble evaluation. numpy/scipy, CPU, seeded.

**Verdict — 5/6 claims verified (10 pts):**
- c1 Thm 1 OW == Bayes-optimal MAP: identical preds K=2,4,6; weight = sigma_K^-1(x_i) (EXACT).
- c2 Thm 2 ISP dominance: E[Adv] ISP>=MV>=SP; closed-form gaps match sim (EXACT).
- c3 Table ISP vs MV: K=2 ISP 90.15 vs MV 84.87 (paper 90.48/85.13); gap slope -0.83.
- c5 16-model OW beats MV: 99.7% of ensembles (paper 97.92%).
- c6 Cor 1 BT weights == logit(x_i) (EXACT).
- c4 real-data OWL: NOT RUN (needs LLM prediction caches).
**Honest negative:** c4 deferred (real-data caches unavailable).
