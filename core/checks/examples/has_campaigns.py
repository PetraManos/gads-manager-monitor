from google.ads.googleads.errors import GoogleAdsException
from ..base import Result, Check, register

@register
class HasCampaigns(Check):
    code = "has_campaigns"
    description = "Customer has at least one non-removed campaign."

    def run(self, provider, customer_id: str) -> Result:
        q = "SELECT campaign.id FROM campaign WHERE campaign.status != 'REMOVED' LIMIT 1"
        try:
            it = provider.gaql(customer_id, q)
            has_any = any(True for _ in it)
            return Result(
                ok=has_any,
                summary="1+ campaign found" if has_any else "No campaigns",
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
