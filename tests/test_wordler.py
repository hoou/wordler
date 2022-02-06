import pytest
from unittest.mock import MagicMock

from wordler import Feedback, SingleFeedback, Wordler


def choose_next(options: list[str]) -> str:
    return next(iter(sorted(options)))


FEEDBACK_MAPPING = {
    "a": SingleFeedback.ABSENT,
    "p": SingleFeedback.PRESENT,
    "c": SingleFeedback.CORRECT,
}


def feedbacks_from_string(feedbacks: list[str]) -> list[Feedback]:
    return [feedback_from_string(feedback) for feedback in feedbacks]


def feedback_from_string(feedback: str) -> Feedback:
    return Feedback(single_feedbacks=[FEEDBACK_MAPPING[f] for f in feedback])


@pytest.mark.parametrize(
    "word_pool, word_attempt, feedback, expected_result",
    (
        (
            ["apple", "apply"],
            "applw",
            feedback_from_string("cccca"),
            ["apple", "apply"],
        ),
        (
            ["apple", "apply"],
            "eppla",
            feedback_from_string("pcccp"),
            ["apple"],
        ),
        (
            ["apple", "apply"],
            "apple",
            feedback_from_string("ccccc"),
            ["apple"],
        ),
        (
            ["phone", "shone"],
            "yhont",
            feedback_from_string("accca"),
            ["phone", "shone"],
        ),
        (
            ["aloft", "alton", "adult", "alert", "alter"],
            "atlas",
            feedback_from_string("cppaa"),
            ["aloft", "alton", "adult", "alert", "alter"],
        ),
        (
            ["apple", "alton", "alert", "alter"],
            "alert",
            feedback_from_string("ccppp"),
            ["alter"],
        ),
    ),
)
def test_get_options(
    word_pool: list[str],
    word_attempt: str,
    feedback,
    expected_result: list[str],
):
    result = Wordler(word_pool, 5, lambda x: Feedback())._get_options(
        word_pool, word_attempt, feedback
    )
    assert set(result) == set(expected_result)


@pytest.mark.parametrize(
    "initial_words, feedbacks, result",
    (
        (
            ["aloft", "alton", "adult", "alert", "alter"],
            feedbacks_from_string(["ccccc"]),
            True,
        ),
        (
            ["aloft", "alter", "alton"],
            feedbacks_from_string(["ccpap", "ccccc"]),
            True,
        ),
        (
            ["frame", "facet", "skill"],
            feedbacks_from_string(["aaaaa", "ccccc"]),
            True,
        ),
        (
            ["frame", "facet", "skill"],
            [Feedback(word_in_list=False), feedback_from_string("ccccc")],
            True,
        ),
        (
            ["aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee", "fffff"],
            feedbacks_from_string(
                ["aaaaa", "aaaaa", "aaaaa", "aaaaa", "aaaaa", "aaaaa"]
            ),
            False,
        ),
    ),
)
def test_solve(
    result: bool,
    initial_words: list[str],
    feedbacks: list[Feedback],
):
    feedback_handler = MagicMock()
    feedback_handler.side_effect = feedbacks
    wordler = Wordler(initial_words, 5, feedback_handler, choose_next)
    assert result == wordler.solve()
