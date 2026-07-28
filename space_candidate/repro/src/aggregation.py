"""LLM aggregation — OW / ISP / MV / SP / OPT (clean-room repro of arXiv 2510.01499).

Model: N agents, M questions, K options. After random label-shuffling: S* ~ Uniform(S);
agent i answers S* w.p. x_i else a uniform wrong option; conditional independence (Assump 1).

Aggregators (closed-form):
  OW  : omega_i = sigma_K^{-1}(x_i) = log(x_i (K-1)/(1-x_i)); argmax_s sum_i omega_i 1{a_i=s}.
  MV  : argmax_s sum_i 1{a_i=s} (tie uniform).
  SP  : Adv_SP(s)  = sum_i 1{a_i=s} - sum_i S_SP(s,i).
  ISP : Adv_ISP(s) = sum_i 1{a_i=s} - sum_i S_ISP(s,i).
  OPT : Bayes-optimal MAP = argmax_s prod_i P(a_i|S*=s)  (== OW under Assumption 1).

Pure numpy, CPU, deterministic given a seed.
"""
from __future__ import annotations
import numpy as np


def sigma_K_inv(x, K):
    """sigma_K^{-1}(x) where sigma_K(x)=e^x/(K-1+e^x).  = log(x (K-1)/(1-x))."""
    return np.log(np.clip(x, 1e-9, 1 - 1e-9) * (K - 1) / np.clip(1 - np.clip(x, 1e-9, 1 - 1e-9), 1e-9, None))


# --------------------------------------------------------------------------- #
#  Data-generating process
# --------------------------------------------------------------------------- #
def simulate(accuracies, K, M, seed=0):
    """Returns truth (M,), answers (M,N) int in [0,K).  Assumption 1 (cond-indep)."""
    rng = np.random.default_rng(seed)
    N = len(accuracies)
    acc = np.asarray(accuracies)
    truth = rng.integers(0, K, size=M)                          # S* uniform after shuffling
    answers = np.empty((M, N), dtype=int)
    for i in range(N):
        correct = rng.random(M) < acc[i]                        # agent i correct?
        # wrong answer: uniform over the K-1 non-truth options
        wrong_opts = np.array([[(o if o < truth[m] else o + 1) for o in range(K - 1)] for m in range(M)])
        pick = rng.integers(0, K - 1, size=M)
        wrong = wrong_opts[np.arange(M), pick]
        answers[:, i] = np.where(correct, truth, wrong)
    return truth, answers


def estimate_pairwise(answers, K):
    """Empirical P(A_i=s | A_j=a) for all i,j,s,a (no ground truth).  Returns P[i,j,s,a]."""
    M, N = answers.shape
    P = np.zeros((N, N, K, K))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for a in range(K):
                mask = answers[:, j] == a
                cnt = mask.sum()
                if cnt > 0:
                    for s in range(K):
                        P[i, j, s, a] = np.mean(answers[mask, i] == s)
                else:
                    P[i, j, s, a] = 1.0 / K
    return P


# --------------------------------------------------------------------------- #
#  Aggregators
# --------------------------------------------------------------------------- #
def agg_mv(answers, K, rng):
    M, N = answers.shape
    out = np.empty(M, dtype=int)
    for m in range(M):
        counts = np.bincount(answers[m], minlength=K)
        mx = counts.max()
        out[m] = rng.choice(np.where(counts == mx)[0])
    return out


def agg_ow(answers, K, accuracies):
    w = sigma_K_inv(accuracies, K)                              # (N,)
    M = answers.shape[0]
    scores = np.zeros((M, K))
    for s in range(K):
        scores[:, s] = (answers == s).astype(float) @ w
    return scores.argmax(axis=1)


def agg_opt(answers, K, accuracies):
    """Bayes-optimal MAP = argmax_s prod_i P(a_i|S*=s).  log-prod = sum log-likelihood."""
    acc = np.clip(accuracies, 1e-9, 1 - 1e-9)
    p_correct = acc
    p_wrong = (1 - acc) / (K - 1)
    M, N = answers.shape
    ll = np.zeros((M, K))
    for s in range(K):
        is_s = (answers == s).astype(float)                     # (M,N)
        ll[:, s] = (is_s * np.log(p_correct) + (1 - is_s) * np.log(p_wrong)) @ np.ones(N)
    return ll.argmax(axis=1)


def _advantage_scores(answers, K, P, variant):
    """Per-question predicted-frequency sum_i S(s,i;m).  Returns (M,K).

    SP : S_SP(s,i;m)  = (1/(N-1)) sum_{j!=i} P[i,j,s, a_j(m)]            (actual answer)
    ISP: S_ISP(s,i;m) = (1/(N-1)) sum_{j!=i} (1/(K-1)) sum_{a!=a_j(m)} P[i,j,s,a]  (counterfactual)
    """
    M, N = answers.shape
    pred = np.zeros((M, K))
    for i in range(N):
        for s in range(K):
            acc = np.zeros(M)
            for j in range(N):
                if j == i:
                    continue
                aj = answers[:, j]                              # (M,)
                if variant == "sp":
                    acc += P[i, j, s, aj]
                else:  # isp
                    rowsum = P[i, j, s, :].sum()
                    acc += (rowsum - P[i, j, s, aj]) / (K - 1)
            acc /= (N - 1)
            pred[:, s] += acc                                   # sum over i
    return pred                                                 # (M,K) = sum_i S(s,i;m)


def agg_advantage(answers, K, P, variant, rng):
    """SP or ISP: f(m) = argmax_s [ sum_i 1{a_i(m)=s} - sum_i S(s,i;m) ]."""
    M, N = answers.shape
    pred = _advantage_scores(answers, K, P, variant)           # (M,K)
    counts = np.zeros((M, K))
    for s in range(K):
        counts[:, s] = (answers == s).sum(axis=1)
    adv = counts - pred
    out = np.empty(M, dtype=int)
    for m in range(M):
        mx = adv[m].max()
        out[m] = rng.choice(np.where(adv[m] == mx)[0])
    return out


def accuracy(pred, truth):
    return float(np.mean(pred == truth))


def expected_advantage(answers, truth, K, P, variant):
    """E[Adv(s*)]: average over questions of Adv(s*) for the true label."""
    M, N = answers.shape
    pred = _advantage_scores(answers, K, P, variant)           # (M,K)
    counts_true = np.array([np.sum(answers[m] == truth[m]) for m in range(M)], dtype=float)
    adv_true = counts_true - pred[np.arange(M), truth]
    return float(np.mean(adv_true))
