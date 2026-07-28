import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import marimo as mo

    return math, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Beyond majority voting: an evidence-first tutorial

    **Headline result:** five of six claims have direct reproducible
    verification. The full paper simulation was rerun at
    \(N=4, M=10{,}000\) over 89 seeds:

    | Setting | Paper ISP | Observed ISP mean | Paper MV | Observed MV mean |
    | --- | ---: | ---: | ---: | ---: |
    | K=2 | 90.48% | **90.16%** | 85.13% | **85.00%** |
    | K=4 | 94.45% | **94.41%** | 92.64% | **92.38%** |

    All four paper values lie inside the empirical single-run 95%
    predictive ranges. Claim 4's exact real-data point estimates remain
    **BLOCKED**, not approximated, because the prediction caches and
    ARMMAN records are unavailable.
    """)
    return


@app.cell
def _(mo):
    accuracy = mo.ui.slider(
        start=0.01, stop=0.99, step=0.01, value=0.75, label="Agent accuracy x"
    )
    choices = mo.ui.slider(
        start=2, stop=10, step=1, value=2, label="Number of options K"
    )
    mo.hstack([accuracy, choices], justify="start")
    return accuracy, choices


@app.cell
def _(accuracy, choices, math, mo):
    weight = math.log(accuracy.value * (choices.value - 1) / (1 - accuracy.value))
    mo.md(
        rf"""
        ## First-order information: the OW weight

        The paper's optimal weight is

        \[
        \omega=\sigma_K^{{-1}}(x)=
        \log\frac{{x(K-1)}}{{1-x}}.
        \]

        For \(x={accuracy.value:.2f}\) and \(K={choices.value}\), the weight is
        **{weight:.4f}**. At \(K=2\), this becomes the Bradley–Terry log-odds
        \(\log(x/(1-x))\).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Second-order information: what ISP changes

    Majority voting counts only the answers. ISP also estimates pairwise
    conditional predictions from the unlabeled question set, asks how
    popular each option would look under counterfactual answers, and
    subtracts that expected popularity from the observed vote.

    The exact proof certificate establishes
    \[
    E[\mathrm{Adv}_{ISP}(s^*)] \ge
    E[\mathrm{Adv}_{MV}(s^*)] \ge
    E[\mathrm{Adv}_{SP}(s^*)]
    \]
    under the paper's shuffled-label, conditional-independence, uniform
    wrong-label, and no-worse-than-random assumptions. A negative control
    puts one agent below random chance and reverses both inequalities.
    """)
    return


@app.cell
def _(mo):
    k_values = [2, 4, 6, 8, 10]
    gap_pp = [5.1599, 2.0367, 1.5537, 1.3407, 1.1926]
    rows = "\n".join(
        f"| {k} | {gap:.4f} pp |" for k, gap in zip(k_values, gap_pp)
    )
    mo.md(
        f"""
        ## Reproduced scaling evidence

        | K | Mean ISP − MV accuracy |
        | ---: | ---: |
        {rows}

        The finite-grid log–log slope is **−0.902**. The theorem's expected
        advantage was checked separately from its exact formula over
        K=16…512, yielding slope **−0.983** and the certified degree-3 over
        degree-4 asymptotic structure.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## What the evidence does—and does not—say

    - **VERIFIED:** OW/MAP optimality, ISP ordering, the full simulation,
      the 47/48 published ensemble aggregate, and the binary
      Bradley–Terry identity.
    - **BLOCKED:** the exact three-dataset OW-L point estimates. Four
      distinct routes could not recover or contradict the same finite
      experiment.
    - **No expensive rerun is required to read this notebook.** All
      displayed results are embedded from the formal evidence.

    To inspect the complete report, open
    `reports/llm-aggregation-reproduction/report.md`. To rerun the fixed
    cumulative verifier locally:

    ```bash
    uv sync --frozen
    uv run python repro/src/verify.py
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
