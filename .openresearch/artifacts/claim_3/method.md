# Claim 3 pilot method

The pilot uses eight fixed seeds, all five paper values of `K`, and an
independently selected extended grid `K={12,16,24,32}`. Every case has the
paper's full `M=10,000`; nothing is downscaled. Pairwise conditionals are
estimated on the same simulated dataset, and ties use a separate deterministic
uniform RNG stream.

Eight worker processes match the documented `cpu-upgrade` vCPU allocation.
The pilot estimates the largest observed standard deviation at K=2 or K=4,
then computes the replicate count needed for a 0.1 percentage-point
normal-approximation half-width. This is a resource calibration based on
observed variance, not a count chosen from the theorem.

An independent slow implementation recreates a full deterministic 256-question
case and must match the production digest. With uniform pairwise information,
ISP must reduce exactly to MV. A sign-corrupted ISP mutation must disagree with
the independent/reference result.
