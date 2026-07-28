# Pinned claims — ZVyd4r9Xl5 "Beyond Majority Voting: LLM Aggregation via Higher-Order Info"

arXiv 2510.01499. No released code (clean-room; aggregators are closed-form).

Model: N agents, M questions, K options. After random label-shuffling: S* ~ Uniform(S);
agent i answers S* w.p. x_i, else a uniform wrong option (1-x_i)/(K-1). Assumption 1:
conditional independence P(A_1..A_N | S*) = prod P(A_i|S*).

## c1 — Theorem 1: OW is Bayes-optimal (first-order).  Algorithm 1.
omega_i = sigma_K^{-1}(x_i), sigma_K(x)=e^x/(K-1+e^x)  =>  omega_i = log( x_i (K-1)/(1-x_i) ).
f_OW = argmax_s sum_i omega_i 1{a_i=s}.
VERIFY (exact): MAP/Bayes-optimal under cond-indep + uniform prior is
  argmax_s prod_i P(a_i|S*=s) ; log-likelihood = sum_i [log x_i 1{a_i=s} + log((1-x_i)/(K-1)) 1{a_i!=s}]
  decision depends on sum_i log( x_i(K-1)/(1-x_i) ) 1{a_i=s} = sum_i omega_i 1{a_i=s}  == OW.
  => OW == Bayes-optimal MAP.  Plus sim: OW accuracy == OPT accuracy.

## c2 — Theorem 2: E[Adv_ISP(s*)] >= E[Adv_MV(s*)] >= E[Adv_SP(s*)].
Closed-form gaps:
  E[Adv_ISP - Adv_MV] = sum_i sum_{j!=i} (Kx_i-1)(Kx_j-1)^2 / [(N-1)K(K-1)^3]   >= 0
  E[Adv_MV - Adv_SP]  = sum_i sum_{j!=i} (Kx_i-1)(Kx_j-1)^2 / [(N-1)K(K-1)^2]   >= 0
  ISP-MV gap shrinks Theta(1/K); MV-SP gap Theta(1).  VERIFY algebraic + sim.

## c3 — Simulation: N=4, x={0.6,0.7,0.8,0.9}, M=10000.  ISP 90.48% vs MV 85.13% (K=2);
       94.45 vs 92.64 (K=4); gap Theta(1/K).  ISP > single-best (0.9).

## c4 — Real data OW-L > MV (UltraFeedback 73.66 vs 72.21, MMLU 90.37 vs 89.32, ARMMAN 85.78 vs 85.24).
       (Best-effort public-data; bonus.)

## c5 — 16-model ensembles: OW-L > MV in 97.92% of cases (+0.54% to +14.20%).  (Sim proxy.)

## c6 — Corollary 1: K=2 optimal weights omega_i ∝ sigma^{-1}(x_i)=logit(x_i) (Bradley-Terry).  (== c1 at K=2.)

## Aggregators
MV: argmax_s sum_i 1{a_i=s}; tie uniform.
SP: Adv_SP(s) = sum_i 1{a_i=s} - sum_i S_SP(s,i);  S_SP(s,i)=(1/(N-1)) sum_{j!=i} P(A_i=s|A_j=a_j).
ISP: Adv_ISP(s)= sum_i 1{a_i=s} - sum_i S_ISP(s,i);
     S_ISP(s,i)=(1/(N-1)) sum_{j!=i} (1/(K-1)) sum_{a!=a_j} P(A_i=s|A_j=a).   [counterfactual avg]
P(A_i=s|A_j=a) estimated empirically from data (no ground truth).
