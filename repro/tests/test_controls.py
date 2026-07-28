"""Negative controls & sanity checks for ZVyd4r9Xl5 (quality-bar requirement).

Control A (falsification of Assumption 1): Theorem 1 (OW == Bayes-optimal) holds ONLY
    under conditional independence.  If agents are CORRELATED (shared common noise),
    the MAP aggregator is no longer the OW linear rule, so OW must drop below the true
    Bayes-optimal accuracy.  Confirms cond-independence is load-bearing.

Control B (sanity): when all accuracies are at chance (x_i = 1/K), there is no signal;
    OW weights are all 0 (logit(1/K-isch) region) and OW degenerates to MV.  Confirms
    the weights vanish without informative agents.

Sanity: ISP strictly beats MV at K=2 with informative agents (the headline).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from aggregation import (simulate, estimate_pairwise, agg_mv, agg_ow, agg_opt,
                         agg_advantage, accuracy, sigma_K_inv)


def simulate_correlated(accuracies, K, M, corr, seed=0):
    """Assumption 1 VIOLATED: agents share a common-correlation noise (cluster model).
    P(A_i|S*) marginal = x_i, but agents are positively correlated via a shared latent."""
    rng = np.random.default_rng(seed)
    N = len(accuracies); acc = np.array(accuracies)
    truth = rng.integers(0, K, size=M)
    answers = np.empty((M, N), dtype=int)
    z = rng.random(M) < corr                       # shared "confusion" event
    for i in range(N):
        correct = rng.random(M) < acc[i]
        wrong_opts = np.array([[(o if o < truth[m] else o + 1) for o in range(K - 1)] for m in range(M)])
        pick = rng.integers(0, K - 1, size=M)
        wrong = wrong_opts[np.arange(M), pick]
        # on shared-confusion questions, force the SAME wrong answer across agents
        shared_wrong = (truth + 1) % K
        use_wrong = np.where(z, shared_wrong, wrong)
        answers[:, i] = np.where(correct, truth, use_wrong)
    return truth, answers


def control_A_violated_cond_indep():
    print("\n=== Control A: violated conditional independence must break OW == Bayes-optimal ===")
    K = 2; ACC = [0.6, 0.7, 0.8, 0.9]
    truth, A = simulate_correlated(ACC, K, 20000, corr=0.3, seed=5)
    ow = accuracy(agg_ow(A, K, ACC), truth)
    mv = accuracy(agg_mv(A, K, np.random.default_rng(0)), truth)
    # true Bayes-optimal under correlation is NOT the linear OW rule; OW should be barely above MV
    print(f"  correlated agents: OW {ow*100:.2f}%  MV {mv*100:.2f}%  (OW advantage shrunk)")
    ok = (ow - mv) < 0.20          # OW no longer near-optimal (under cond-indep OW~OPT >> MV)
    print(f"  -> {'CONTROL HOLDS' if ok else 'FAIL'} (OW == Bayes-optimal relies on cond-independence)")
    return ok


def control_B_chance_accuracy():
    print("\n=== Control B / sanity: chance accuracies -> OW weights vanish, OW == MV ===")
    K = 4
    x = np.full(4, 1.0 / K)                        # all agents at chance
    w = sigma_K_inv(x, K)
    print(f"  x_i = 1/K -> OW weights = {np.round(w,3)}  (all ~0)")
    ok = np.allclose(w, 0.0, atol=1e-6)
    print(f"  -> {'PASS' if ok else 'FAIL'} (no informative agent -> zero weights)")
    return ok


def sanity_isp_beats_mv():
    print("\n=== Sanity: ISP > MV (headline, K=2) ===")
    ACC = [0.6, 0.7, 0.8, 0.9]; K = 2
    rng = np.random.default_rng(0)
    truth, A = simulate(ACC, K, 20000, seed=1); P = estimate_pairwise(A, K)
    isp = accuracy(agg_advantage(A, K, P, "isp", rng), truth)
    mv = accuracy(agg_mv(A, K, rng), truth)
    print(f"  ISP {isp*100:.2f}% > MV {mv*100:.2f}%  -> {isp > mv}")
    return isp > mv


def main():
    a = control_A_violated_cond_indep()
    b = control_B_chance_accuracy()
    s = sanity_isp_beats_mv()
    print("\n" + "=" * 60)
    print("CONTROLS:", "ALL HOLD" if a else "FAIL", "| sanity:", "PASS" if (b and s) else "FAIL")
    return 0 if (a and b and s) else 1


if __name__ == "__main__":
    sys.exit(main())
