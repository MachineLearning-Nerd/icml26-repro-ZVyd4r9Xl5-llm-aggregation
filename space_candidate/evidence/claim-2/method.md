# Claim 2 method

The production certificate reconstructs the paper's same-answer and
different-answer pairwise conditionals as rational functions of symbolic
`K`, `x`, and `y`. A dependency-free sparse-polynomial engine clears the
denominators and checks both contribution identities exactly. Summing those
identities over ordered pairs gives the two displayed N-agent formulas.

The ordering then follows because `K*x_i-1 >= 0`, squares are nonnegative,
and the denominators are positive for `N>=2`, `K>=2`.

The independent checker imports no production aggregation code. It enumerates
every answer profile in four exact-rational finite domains, reconstructs
pairwise conditionals from the generative distribution, evaluates ISP/MV/SP
from their definitions, and integrates over every truth and answer profile.

The negative control keeps the shuffle symmetry, uniform errors, and
conditional independence, but gives one binary agent accuracy `2/5 < 1/2`.
Both theorem inequalities must reverse. Observing that reversal confirms the
checker can fail for the intended, premise-specific reason.
