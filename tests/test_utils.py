from utils import get_config_value


def test_get_config_value_returns_str(monkeypatch) -> None:
    """
    Checks get_config_value returns a string (may be empty) for a given key.
    """

    # Patch Path.open to return a fake config.json content as a file-like object
    class DummyFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return '{"BUCKET": "test-bucket"}'

    monkeypatch.setattr("utils.Path.open", lambda self, *a, **k: DummyFile())
    value = get_config_value("BUCKET")
    assert isinstance(value, str)
    assert value == "test-bucket"
