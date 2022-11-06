import numpy as np
import pytest

from main import PoseAnalyzer

PRED_COORD = np.array(
    [
        [188.59113, 153.49432],
        [188.59113, 138.86145],
        [184.23267, 138.86145],
        [210.38342, 146.17786],
        [232.17572, 131.54498],
        [214.74188, 212.02588],
        [267.0434, 175.44366],
        [197.30804, 299.82318],
        [249.60956, 241.29163],
        [153.72345, 270.5574],
        [192.94958, 233.97519],
        [245.2511, 372.9876],
        [280.11877, 336.4054],
        [258.32648, 446.15204],
        [297.5526, 438.83557],
        [258.32648, 482.7342],
        [319.3449, 482.7342],
    ],
    dtype="float32",
)


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        (np.array([1, 0]), np.array([0, 0]), np.array([1, 1]), 45),
        (np.array([1, 0]), np.array([0, 0]), np.array([1, 0]), 0),
        (np.array([1, 0]), np.array([0, 0]), np.array([0, 1]), 90),
    ],
)
def test_calc_angle_at_b(a, b, c, expected):
    assert PoseAnalyzer("test.jpg").calc_angle_at_b(a, b, c) == expected


def test_calc_spine_nose_angle():
    assert PoseAnalyzer("test.jpg").calc_spine_nose_angle(PRED_COORD) == 135


def test_predict_feature_coords():
    pred_coords = PoseAnalyzer("test.jpg").predict_feature_coords()
    np.testing.assert_array_equal(pred_coords, PRED_COORD)
