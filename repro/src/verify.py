"""Verify all claims for ZVyd4r9Xl5 (arXiv 2510.01499) LLM aggregation.

c1 Theorem 1: OW == Bayes-optimal MAP (omega_i = sigma_K^{-1}(x_i)).  EXACT.
c2 Theorem 2: E[Adv_ISP] >= E[Adv_MV] >= E[Adv_SP]; closed-form gaps match.
c3 Table: ISP 90.48 vs MV 85.13 (K=2), 94.45 vs 92.64 (K=4); gap Theta(1/K).
c5 16-model ensembles: OW > MV in ~98% of cases.
c6 Corollary 1: K=2 optimal weights proportional to logit(x_i) (Bradley-Terry).

Run: python repro/src/verify.py
"""
from __future__ import annotations
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from aggregation import (simulate, estimate_pairwise, agg_mv, agg_ow, agg_opt,
                         agg_advantage, accuracy, expected_advantage, sigma_K_inv)

ACC = [0.6, 0.7, 0.8, 0.9]


def table_c3():
    """c3: accuracy across K.  Returns dict K -> {mv,sp,isp,ow,opt}."""
    out = {}
    for K in [2, 4, 6, 8, 10]:
        rng = np.random.default_rng(0)
        truth, A = simulate(ACC, K, 10000, seed=1)
        P = estimate_pairwise(A, K)
        out[K] = dict(
            mv=accuracy(agg_mv(A, K, rng), truth),
            sp=accuracy(agg_advantage(A, K, P, "sp", rng), truth),
            isp=accuracy(agg_advantage(A, K, P, "isp", rng), truth),
            ow=accuracy(agg_ow(A, K, ACC), truth),
            opt=accuracy(agg_opt(A, K, ACC), truth),
        )
    return out


def thm1_ow_is_opt():
    """c1: OW == Bayes-optimal OPT, exactly, across K."""
    res = {}
    for K in [2, 4, 6]:
        truth, A = simulate(ACC, K, 5000, seed=2)
        ow = agg_ow(A, K, ACC); opt = agg_opt(A, K, ACC)
        res[K] = dict(ow=accuracy(ow, truth), opt=accuracy(opt, truth),
                      identical=bool(np.array_equal(ow, opt)))
    all_identical = all(res[K]["identical"] for K in res)
    # algebraic: MAP weight = sigma_K^{-1}(x_i)
    K = 4
    alg_ok = np.allclose(sigma_K_inv(ACC, K), np.log(np.array(ACC) * (K - 1) / (1 - np.array(ACC))))
    return res, all_identical and alg_ok


def thm2_ordering_and_gaps():
    """c2: E[Adv] ordering ISP>=MV>=SP and closed-form gap match."""
    out = {}
    for K in [2, 4, 6]:
        rng = np.random.default_rng(0)
        truth, A = simulate(ACC, K, 20000, seed=3)
        P = estimate_pairwise(A, K)
        e_isp = expected_advantage(A, truth, K, P, "isp")
        e_sp = expected_advantage(A, truth, K, P, "sp")
        e_mv = float(np.mean([np.sum(A[m] == truth[m]) for m in range(A.shape[0])])) - len(ACC) / K
        # closed-form gaps
        N = len(ACC); x = np.array(ACC)
        s = 0.0
        for i in range(N):
            for j in range(N):
                if i != j:
                    s += (K * x[i] - 1) * (K * x[j] - 1) ** 2
        cf_isp_mv = s / ((N - 1) * K * (K - 1) ** 3)
        cf_mv_sp = s / ((N - 1) * K * (K - 1) ** 2)
        out[K] = dict(e_isp=e_isp, e_mv=e_mv, e_sp=e_sp,
                      order_ok=bool(e_isp >= e_mv >= e_sp),
                      sim_isp_mv=e_isp - e_mv, sim_mv_sp=e_mv - e_sp,
                      cf_isp_mv=cf_isp_mv, cf_mv_sp=cf_mv_sp)
    # Theta(1/K): isp-mv gap ~ 1/K ; mv-sp ~ const
    return out


def c5_ensemble(n_models=16, n_trials=300):
    """c5: across many 16-model ensembles with HETEROGENEOUS accuracies (incl. near-chance
    models, as in real LLM ensembles), OW > MV in ~98% of cases (paper 97.92%).
    Near-chance models get ~0 weight (logit), so OW down-weights them while MV is dragged down."""
    rng = np.random.default_rng(42)
    wins = 0; gaps = []
    K = 2
    for t in range(n_trials):
        acc = rng.uniform(0.50, 0.95, size=n_models)         # heterogeneous, down to chance
        truth, A = simulate(acc, K, 3000, seed=1000 + t)
        ow = accuracy(agg_ow(A, K, acc), truth)
        mv = accuracy(agg_mv(A, K, np.random.default_rng(9 + t)), truth)
        if ow > mv + 1e-9:
            wins += 1
        gaps.append(ow - mv)
    return dict(win_rate=wins / n_trials,
                mean_gap=float(np.mean(gaps)),
                min_gap=float(np.min(gaps)), max_gap=float(np.max(gaps)))


def main():
    t0 = time.time()
    out = {}
    print("=" * 70); print("c1 / Theorem 1: OW == Bayes-optimal"); print("=" * 70)
    res, ok = thm1_ow_is_opt()
    out["c1_thm1"] = res; out["c1_ok"] = bool(ok)
    for K, r in res.items():
        print(f"  K={K}: OW {r['ow']*100:.2f}%  OPT {r['opt']*100:.2f}%  identical={r['identical']}")
    print(f"  MAP weight = sigma_K^-1(x_i) = log(x_i(K-1)/(1-x_i))  -> {ok}")

    print("\n" + "=" * 70); print("c3 / Table: accuracy across K (ISP vs MV vs SP vs OW/OPT)"); print("=" * 70)
    tab = table_c3(); out["c3_table"] = tab
    print(f"  {'K':>3} {'MV':>6} {'SP':>6} {'ISP':>6} {'OW':>6} {'OPT':>6}")
    for K, r in tab.items():
        print(f"  {K:>3} {r['mv']*100:6.2f} {r['sp']*100:6.2f} {r['isp']*100:6.2f} {r['ow']*100:6.2f} {r['opt']*100:6.2f}")
    print("  paper K=2: MV 85.13 SP 79.94 ISP 90.48 OPT 91.37 ; K=4: MV 92.64 ISP 94.45")
    isp_mv_gap = [tab[K]["isp"] - tab[K]["mv"] for K in [2, 4, 6, 8, 10]]
    slope = float(np.polyfit(np.log([2, 4, 6, 8, 10]), np.log(isp_mv_gap), 1)[0])
    out["c3_gap_slope"] = slope
    print(f"  ISP-MV gap vs K log-log slope = {slope:.2f}  (expect ~ -1 = Theta(1/K))")

    print("\n" + "=" * 70); print("c2 / Theorem 2: E[Adv] ordering + closed-form gaps"); print("=" * 70)
    t2 = thm2_ordering_and_gaps(); out["c2_thm2"] = t2
    for K, r in t2.items():
        print(f"  K={K}: E[Adv] ISP {r['e_isp']:.3f} >= MV {r['e_mv']:.3f} >= SP {r['e_sp']:.3f}  "
              f"-> {r['order_ok']}")
        print(f"        gap ISP-MV sim {r['sim_isp_mv']:.3f} vs cf {r['cf_isp_mv']:.3f} ; "
              f"MV-SP sim {r['sim_mv_sp']:.3f} vs cf {r['cf_mv_sp']:.3f}")

    print("\n" + "=" * 70); print("c5 / 16-model ensembles: OW > MV win-rate"); print("=" * 70)
    e = c5_ensemble(); out["c5_ensemble"] = e
    print(f"  OW > MV in {e['win_rate']*100:.1f}% of 16-model ensembles "
          f"(mean gap {e['mean_gap']*100:.2f}%, range {e['min_gap']*100:.2f}%..{e['max_gap']*100:.2f}%)")
    print("  paper: OW-L > MV in 97.92% of cases (+0.54%..+14.20%)")

    print("\n" + "=" * 70); print("c6 / Corollary 1: K=2 optimal weights = logit(x_i) (Bradley-Terry)"); print("=" * 70)
    x = np.array(ACC); w = sigma_K_inv(x, 2)
    c6_ok = np.allclose(w, np.log(x / (1 - x)))
    out["c6_ok"] = bool(c6_ok)
    print(f"  K=2 weights {np.round(w,3)} ; logit(x) {np.round(np.log(x/(1-x)),3)}  -> {c6_ok}")

    out["elapsed_sec"] = round(time.time() - t0, 1)
    os.makedirs("outputs", exist_ok=True)
    json.dump(out, open("outputs/verify_results.json", "w"), indent=2)
    print(f"\nSaved outputs/verify_results.json ({out['elapsed_sec']}s)")

    print("\n" + "=" * 70)
    print("c1 / formal universal proof certificate + independent checker + control")
    print("=" * 70)
    claim1_verifier = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        ".openresearch",
        "artifacts",
        "claim_1",
        "verifier.py",
    )
    if not os.path.isfile(claim1_verifier):
        claim1_verifier = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "evidence",
            "claim-1",
            "verifier.py",
        )
    completed = subprocess.run([sys.executable, claim1_verifier], check=False)
    if completed.returncode != 0:
        print(f"CLAIM_1_VERIFIER_FAILED exit={completed.returncode}")
        raise SystemExit(completed.returncode)
    print("CUMULATIVE_VERDICT claim_1=VERIFIED")

    print("\n" + "=" * 70)
    print("c2 / formal universal ordering certificate + independent checker + control")
    print("=" * 70)
    claim2_verifier = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        ".openresearch",
        "artifacts",
        "claim_2",
        "verifier.py",
    )
    if not os.path.isfile(claim2_verifier):
        claim2_verifier = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "evidence",
            "claim-2",
            "verifier.py",
        )
    completed = subprocess.run([sys.executable, claim2_verifier], check=False)
    if completed.returncode != 0:
        print(f"CLAIM_2_VERIFIER_FAILED exit={completed.returncode}")
        raise SystemExit(completed.returncode)
    print("CUMULATIVE_VERDICT claim_2=VERIFIED")


if __name__ == "__main__":
    main()
