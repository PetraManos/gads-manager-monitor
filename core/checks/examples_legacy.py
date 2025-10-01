from typing import Iterable, Dict, Any
from .base import register, Check

@register
class NoEnabledCampaigns(Check):
    code = "no_enabled_campaigns"
    desc = "Account has zero ENABLED campaigns."

    def run(self, client, customer_id: str) -> Iterable[Dict[str, Any]]:
        svc = client.get_service("GoogleAdsService")
        q = """
            SELECT campaign.id, campaign.status
            FROM campaign
            WHERE campaign.status = 'ENABLED'
            LIMIT 1
        """
        rows = svc.search(customer_id=customer_id, query=q)
        has_enabled = False
        for _ in rows:
            has_enabled = True
            break
        if not has_enabled:
            yield {
                "severity": "WARN",
                "message": "No ENABLED campaigns in account.",
                "evidence": {"query": q.strip()},
            }
