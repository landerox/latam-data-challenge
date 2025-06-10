from datetime import date
import pytest

from q1_memory import q1_memory
from q1_time import q1_time


@pytest.fixture
def fake_tweets_file(tmp_path) -> str:
    """
    Creates a fake JSONL tweet file for testing.
    """
    lines = [
        '{"date": "2021-02-01T12:00:00Z", "user": {"username": "alice"}}\n',
        '{"date": "2021-02-01T15:00:00Z", "user": {"username": "alice"}}\n',
        '{"date": "2021-02-01T18:00:00Z", "user": {"username": "bob"}}\n',
        '{"date": "2021-02-02T09:00:00Z", "user": {"username": "carol"}}\n',
        '{"date": "2021-02-02T10:00:00Z", "user": {"username": "carol"}}\n',
        '{"date": "2021-02-02T11:00:00Z", "user": {"username": "dan"}}\n',
    ]
    path = tmp_path / "tweets.jsonl"
    path.write_text("".join(lines), encoding="utf-8")
    return str(path)


def test_q1_memory_output(fake_tweets_file) -> None:
    """
    Checks q1_memory returns the expected top N days and users.
    """
    res = q1_memory(fake_tweets_file, top_n=2)
    assert isinstance(res, list)
    assert all(isinstance(t, tuple) for t in res)
    assert len(res) == 2
    assert all(isinstance(d, date) and isinstance(u, str) for d, u in res)
    # The day with the most tweets: 2021-02-01 (alice should be top user)
    assert res[0][1] == "alice"


def test_q1_time_output(fake_tweets_file) -> None:
    """
    Checks q1_time returns the expected top N days and users.
    """
    res = q1_time(fake_tweets_file, top_n=2)
    assert isinstance(res, list)
    assert all(isinstance(t, tuple) for t in res)
    assert len(res) == 2
    assert all(isinstance(d, date) and isinstance(u, str) for d, u in res)
    assert res[0][1] == "alice"
