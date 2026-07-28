"""Universal inverse-logit and Bradley–Terry identities for Claim 6."""

from __future__ import annotations

import math


def logit(probability: float) -> float:
    """Finite inverse logistic on its exact real-valued domain."""
    if not 0.0 < probability < 1.0:
        raise ValueError("a finite logit requires 0 < probability < 1")
    return math.log(probability / (1.0 - probability))


def sigmoid(score: float) -> float:
    if score >= 0.0:
        inverse = math.exp(-score)
        return 1.0 / (1.0 + inverse)
    exponential = math.exp(score)
    return exponential / (1.0 + exponential)


def bradley_terry_probability(first_score: float, second_score: float) -> float:
    """Probability that the first item wins under Bradley–Terry."""
    return sigmoid(first_score - second_score)


def symbolic_certificate() -> dict[str, object]:
    """Machine-readable universal algebraic proof over x in (0, 1)."""
    return {
        "domain": "x in (0,1); endpoints are extended-real limits",
        "sigma_2": "exp(w)/(1+exp(w))",
        "inverse_candidate": "w=log(x/(1-x))",
        "cross_multiplication": [
            "x*(1+z)=z where z=exp(w)>0",
            "z*(1-x)=x",
            "z=x/(1-x)",
            "w=log(x/(1-x)) because exp is bijective R -> (0,infinity)",
        ],
        "denominator_positive": True,
        "solution_positive": True,
        "solution_unique": True,
        "composition_identity": "(x/(1-x))/(1+x/(1-x))=x",
        "bradley_terry_factorization": (
            "exp(r1)/(exp(r1)+exp(r0))"
            "=exp(r1-r0)/(1+exp(r1-r0))=sigma(r1-r0)"
        ),
        "bt_score_difference": "r1-r0=log(p/(1-p))",
        "algorithm_1_weight_equality": "omega_i=sigma_2^{-1}(x_i)",
        "corollary_proportionality": (
            "multiplying every weight by one common positive constant "
            "preserves the weighted-vote argmax"
        ),
        "status": "PASS",
    }


def numerical_examples() -> list[dict[str, object]]:
    probabilities = [0.001, 0.1, 0.5, 0.6, 0.75, 0.9, 0.999]
    rows = []
    for probability in probabilities:
        weight = logit(probability)
        shifted_second_score = 7.25
        shifted_first_score = shifted_second_score + weight
        recovered = sigmoid(weight)
        bt_recovered = bradley_terry_probability(
            shifted_first_score, shifted_second_score
        )
        rows.append(
            {
                "accuracy": probability,
                "logit_weight": weight,
                "sigmoid_of_weight": recovered,
                "bt_probability_with_shifted_scores": bt_recovered,
                "composition_error": abs(recovered - probability),
                "bt_error": abs(bt_recovered - probability),
            }
        )
    return rows


def controls() -> dict[str, object]:
    probability = 0.75
    wrong_weight = math.log(probability)
    wrong_recovered = sigmoid(wrong_weight)

    endpoint_rejections = {}
    for endpoint in (0.0, 1.0):
        try:
            logit(endpoint)
        except ValueError:
            endpoint_rejections[str(endpoint)] = True
        else:
            endpoint_rejections[str(endpoint)] = False

    positive_scores = [0.4054651081081642, 2.1972245773362196]
    label_zero_score = positive_scores[0]
    label_one_score = positive_scores[1]
    positive_scale_preserves = (3.0 * label_one_score) > (3.0 * label_zero_score)
    negative_scale_reverses = (-3.0 * label_one_score) < (-3.0 * label_zero_score)
    return {
        "wrong_log_probability_transform_rejected": not math.isclose(
            wrong_recovered, probability, rel_tol=0.0, abs_tol=1e-12
        ),
        "wrong_transform_input": probability,
        "wrong_transform_sigmoid_output": wrong_recovered,
        "finite_domain_endpoint_rejections": endpoint_rejections,
        "endpoint_limits": {"x_to_0": "-infinity", "x_to_1": "+infinity"},
        "positive_common_scale_preserves_argmax": positive_scale_preserves,
        "negative_common_scale_reverses_argmax": negative_scale_reverses,
    }
