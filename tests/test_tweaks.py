from neonctl.backend.tweaks import TweaksService


def test_tweaks_catalog_size_and_lru_gen():
    svc = TweaksService()
    items = svc.available_tweaks()
    assert len(items) >= 21
    ids = {t["id"] for t in items}
    assert "lru_gen_ttl_200" in ids


def test_apply_tweak_unknown_returns_none():
    svc = TweaksService()
    assert svc.apply_tweak("missing") is None
