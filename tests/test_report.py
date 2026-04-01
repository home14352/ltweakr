from neonctl.backend.report import diagnostics_report


def test_diagnostics_report_contains_header():
    out = diagnostics_report()
    assert "NeonCtl Diagnostics Report" in out
    assert "Native manager:" in out
