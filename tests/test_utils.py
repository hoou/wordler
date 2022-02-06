import pytest

from wordlerer import utils


@pytest.mark.parametrize(
    "words, length, expected",
    (
        (["car", "boat", "bike", "helicopter"], 4, ["boat", "bike"]),
        (["car", "boat", "bike", "helicopter"], 3, ["car"]),
    ),
)
def test_filter_by_length(words: list[str], length: int, expected: list[str]):
    assert utils.filter_by_length(words, length) == expected
