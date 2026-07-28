# Limitations and deviations

The Bradley-Terry connection is an algebraic identity, not evidence that every
real LLM preference process satisfies a Bradley-Terry data-generating model.
Additive score offsets are unidentifiable in Bradley-Terry, and a common
positive scale can be absorbed as temperature. The paper writes
“proportional”; Algorithm 1 supplies equality under its chosen normalization.

Perfect accuracy `x=1` has an infinite logit. The verifier treats it only as an
extended-real limit and never presents it as a finite implementable weight.
