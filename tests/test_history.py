from neonctl.backend import history


def test_history_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "history_path", lambda: tmp_path / "history.log")
    history.append_history("apt search nano", True, "Search nano")
    rows = history.read_history(limit=10)
    assert len(rows) == 1
    assert rows[0].success is True
    assert "apt" in rows[0].command
