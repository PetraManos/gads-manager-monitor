from google.ads.googleads.errors import GoogleAdsException
from ..base import Result, Check, register

@register
class NoEnabledCampaigns(Check):
    code = "no_enabled_campaigns"
    description = "Flags when the customer has zero ENABLED campaigns."

    def run(self, provider, customer_id: str) -> Result:
        q = "SELECT campaign.id FROM campaign WHERE campaign.status = 'ENABLED' LIMIT 1"
        try:
            any_enabled = any(True for _ in provider.gaql(customer_id, q))
            ok = not any_enabled  # ok=True means the condition holds: no enabled campaigns
            return Result(
                ok=ok,
                summary=("No enabled campaigns" if ok else "Has at least one enabled campaign"),
                details={"query": q},
                code=self.code,
                customer_id=str(customer_id),
            )
        except GoogleAdsException as e:
            return Result(
                ok=False,
                summary="Google Ads API error",
                details={"message": str(e)},
                code=self.code,
                customer_id=str(customer_id),
            )
