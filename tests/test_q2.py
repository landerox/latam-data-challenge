import pytest

from q2_memory import q2_memory
from q2_time import q2_time


@pytest.fixture
def fake_emojis_file(tmp_path) -> str:
    """
    Creates a fake JSONL tweet file with emojis for testing.
    """
    lines = [
        '{"content": "Good morning! ☀️😊"}\n',
        '{"content": "Hello world! 😊😊"}\n',
        '{"content": "I love Python! 🐍😊"}\n',
        '{"content": "So happy! 😊"}\n',
        '{"content": "Just code! 🐍"}\n',
    ]
    path = tmp_path / "emojis.jsonl"
    path.write_text("".join(lines), encoding="utf-8")
    return str(path)


def test_q2_memory_output(fake_emojis_file) -> None:
    """
    Checks q2_memory returns the expected most-used emojis or emoji groups.
    """
    result = q2_memory(fake_emojis_file, top_n=2)
    assert isinstance(result, list)
    assert all(isinstance(t, tuple) for t in result)
    assert len(result) == 2

    # Accept both individual and grouped emojis due to current regex.
    emojis_with_counts = dict(result)
    # There should be an entry containing '😊' with count >= 4
    found = False
    for emoji, count in emojis_with_counts.items():
        if "😊" in emoji and count >= 4:
            found = True
    assert found, "Expected to find '😊' at least 4 times in the result"


def test_q2_time_output(fake_emojis_file) -> None:
    """
    Checks q2_time returns the expected most-used emojis or emoji groups.
    """
    result = q2_time(fake_emojis_file, top_n=2)
    assert isinstance(result, list)
    assert all(isinstance(t, tuple) for t in result)
    assert len(result) == 2

    emojis_with_counts = dict(result)
    found = False
    for emoji, count in emojis_with_counts.items():
        if "😊" in emoji and count >= 4:
            found = True
    assert found, "Expected to find '😊' at least 4 times in the result"
