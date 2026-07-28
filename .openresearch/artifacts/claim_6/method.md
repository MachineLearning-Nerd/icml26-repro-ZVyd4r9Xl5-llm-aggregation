# Method

The formal certificate substitutes `z=exp(w)>0` into
`x=z/(1+z)`, cross-multiplies, and solves uniquely:
`z=x/(1-x)`, hence `w=log(x/(1-x))`. It independently factors the
Bradley-Terry probability by a positive `exp(r_0)` to obtain
`sigma(r_1-r_0)`.

A separate checker imports no production code. It uses exact rational odds for
six probabilities and an independent 60-digit Decimal `ln`/`exp` route.

Controls reject `log(x)` as a substitute for log-odds, enforce the finite
endpoint domain, verify that a positive common scale preserves weighted-vote
argmax, and show that a negative scale reverses it.
