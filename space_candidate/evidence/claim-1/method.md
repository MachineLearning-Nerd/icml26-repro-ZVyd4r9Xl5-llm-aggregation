# Claim 1 method

The verifier reconstructs the Bayes rule from the stated generative model. For
candidate label `s`, write `v_i(s)=1{a_i=s}`. Conditional independence gives

`L_s = product_i x_i^v_i(s) * ((1-x_i)/(K-1))^(1-v_i(s))`.

Each factor is rewritten exactly as

`((1-x_i)/(K-1)) * (x_i*(K-1)/(1-x_i))^v_i(s)`.

The first product is positive and independent of `s`. The uniform prior is also
independent of `s`, so both cancel from the posterior ordering. Applying the
strictly increasing logarithm leaves

`sum_i log(x_i*(K-1)/(1-x_i)) * 1{a_i=s}`,

which is exactly Algorithm 1 because solving
`x = exp(z)/(K-1+exp(z))` gives
`z = log(x*(K-1)/(1-x))`.

The JSON proof certificate encodes the exponents as affine functions of the
generic vote indicator and the verifier checks both symbolic sides. A separate
implementation exhausts every answer profile for five rational test families
using `fractions.Fraction`; it never imports the aggregation implementation.
The negative control keeps a uniform prior and 70% marginal accuracy for every
agent but introduces conditional dependence, producing an intentional OW/MAP
disagreement.
