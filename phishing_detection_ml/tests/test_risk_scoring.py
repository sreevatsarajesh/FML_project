import pytest
from src.risk_scoring import Calc_Risk

@pytest.mark.parametrize(
    ("probability", "expected_level"),
    [
        (0.00, "Very Low"),
        (0.09, "Very Low"),
        (0.10, "Low"),
        (0.19, "Low"),
        (0.20, "Medium"),
        (0.29, "Medium"),
        (0.30, "High"),
        (0.75, "High"),
        (1.00, "High"),
    ],
)
def test_risk_levels(probability, expected_level):
    result = Calc_Risk(probability, threshold=0.3)
    assert result["Risk Level"] == expected_level
    assert result["Probability"] == probability
    assert result["Risk Score"] == probability * 100

def test_threshold_boundary_is_high():
    result = Calc_Risk(0.3, threshold=0.3)
    assert result["Risk Level"] == "High"

def test_custom_threshold():
    result = Calc_Risk(0.25, threshold=0.2)
    assert result["Risk Level"] == "High"

@pytest.mark.parametrize("probability", [-0.1, 1.1])
def test_out_of_range_probability_is_rejected(probability):
    # Enable this test after adding input validation to Calc_Risk.
    with pytest.raises(ValueError):
        Calc_Risk(probability)
