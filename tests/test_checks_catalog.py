from core.checks.base import list_codes
import core.checks.examples  # registers checks

def test_catalog_nonempty():
    assert "no_enabled_campaigns" in list_codes()
