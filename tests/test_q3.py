import pytest

from q3_memory import q3_memory
from q3_time import q3_time


@pytest.fixture
def fake_mentions_file(tmp_path) -> str:
    """
    Creates a fake JSONL tweet file with mentioned users for testing.
    """
    lines = [
        '{"mentionedUsers": [{"username": "alice"}]}\n',
        '{"mentionedUsers": [{"username": "bob"}, {"username": "alice"}]}\n',
        '{"mentionedUsers": [{"username": "alice"}]}\n',
        '{"mentionedUsers": [{"username": "carol"}]}\n',
        '{"mentionedUsers": [{"username": "bob"}]}\n',
    ]
    path = tmp_path / "mentions.jsonl"
    path.write_text("".join(lines), encoding="utf-8")
    return str(path)


def test_q3_memory_output(fake_mentions_file) -> None:
    """
    Checks q3_memory returns the top mentioned usernames and correct counts.
    """
    result = q3_memory(fake_mentions_file, top_n=2)
    assert isinstance(result, list)
    assert all(isinstance(t, tuple) for t in result)
    assert len(result) == 2
    result_dict = dict(result)
    assert "alice" in result_dict
    assert result_dict["alice"] == 3
    # bob (2) or carol (1) should be present as the other top username
    assert any(u in result_dict for u in ("bob", "carol"))


def test_q3_time_output(fake_mentions_file) -> None:
    """
    Checks q3_time returns the top mentioned usernames and correct counts.
    """
    result = q3_time(fake_mentions_file, top_n=2)
    assert isinstance(result, list)
    assert all(isinstance(t, tuple) for t in result)
    assert len(result) == 2
    result_dict = dict(result)
    assert "alice" in result_dict
    assert result_dict["alice"] == 3
    assert any(u in result_dict for u in ("bob", "carol"))
