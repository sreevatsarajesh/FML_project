import pytest
from src.fusion_v2 import (
    NUMERIC_WEIGHT,
    THRESHOLD,
    TRUSTED_RISK_CAP,
    _is_trusted_root,
    predict_fused_url,
)

def test_numeric_weight_is_valid():
    assert 0.0 <= NUMERIC_WEIGHT <= 1.0

def test_threshold_is_valid():
    assert 0.0 <= THRESHOLD <= 1.0

def test_trusted_risk_cap_is_valid():
    assert 0.0 <= TRUSTED_RISK_CAP <= 1.0

@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/",
        "https://google.com/",
    ],
)
def test_trusted_root_is_recognized(url):
    assert _is_trusted_root(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/attacker/repo",
        "https://github.com/attacker/repo/",
        "https://gist.github.com/",
        "https://github.com.example.com/",
        "https://attacker.github.com/",
        "https://github.com/?next=example",
        "https://github.com/#section",
        "https://user:password@github.com/",
    ],
)
def test_non_root_or_excluded_urls_are_not_trusted_roots(url):
    assert _is_trusted_root(url) is False


@pytest.mark.parametrize(
    "url",
    [
        "",
        "   ",
        None,
        123,
    ],
)
def test_invalid_urls_are_rejected(url):
    with pytest.raises(ValueError):
        predict_fused_url(url)

@pytest.mark.parametrize("weight", [-0.01, 1.01])
def test_invalid_numeric_weights_are_rejected(weight):
    with pytest.raises(ValueError):
        predict_fused_url("https://example.com/", numeric_weight=weight)


def test_prediction_returns_expected_fields():
    result = predict_fused_url("https://example.com/")

    expected_keys = {
        "numeric_probability",
        "nlp_probability",
        "model_probability",
        "fused_probability",
        "numeric_weight",
        "trusted_domain",
        "prediction",
    }
    assert expected_keys.issubset(result.keys())

def test_probabilities_are_in_valid_range():
    result = predict_fused_url("https://example.com/")
    for key in (
        "numeric_probability",
        "nlp_probability",
        "model_probability",
        "fused_probability",
    ):
        assert 0.0 <= result[key] <= 1.0

def test_fusion_probability_matches_weighted_average():
    result = predict_fused_url("https://example.com/")
    expected = (
        result["numeric_weight"] * result["numeric_probability"]
        + (1.0 - result["numeric_weight"]) * result["nlp_probability"]
    )
    assert result["model_probability"] == pytest.approx(expected)

def test_prediction_matches_threshold():
    result = predict_fused_url("https://example.com/")
    expected = (
        "phishing"
        if result["fused_probability"] >= THRESHOLD
        else "benign"
    )

    assert result["prediction"] == expected