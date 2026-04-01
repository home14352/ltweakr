from neonctl.backend.monitoring import collect_stats


def test_collect_stats():
    s = collect_stats()
    assert "cpu_percent" in s
