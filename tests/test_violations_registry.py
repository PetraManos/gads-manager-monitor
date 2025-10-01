from core.violations.registry import registry, register
from dataclasses import dataclass
from core.violations.base import ViolationResult

def test_registry_lists_codes():
    codes = registry.list()
    # our example checks should be present
    assert "no_recent_impressions_14d" in codes
    assert "disapproved_ads_present" in codes

def test_duplicate_registration_raises():
    @dataclass
    class Dummy:
        code: str = "dup_code"
        description: str = "d"
        def run(self, customer_id: str, **params) -> ViolationResult:
            return ViolationResult(False, {})
    # first time ok
    register(Dummy())
    # second time should raise
    try:
        register(Dummy())
        raise AssertionError("Expected ValueError on duplicate registration")
    except ValueError:
        pass
