from dataclasses import dataclass
from core.violations.base import ViolationResult
from core.violations.registry import register

@dataclass
class DisapprovedAds:
    code: str = "disapproved_ads_present"
    description: str = "Any ENABLED ad group contains disapproved ads"
    client: object | None = None

    def run(self, customer_id: str, **params) -> ViolationResult:
        # Placeholder GAQL; implement real logic in next step
        return ViolationResult(False, {"entities": [], "meta": {}})

register(DisapprovedAds())
