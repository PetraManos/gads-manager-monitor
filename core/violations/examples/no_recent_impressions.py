from dataclasses import dataclass
from typing import Any, Iterable
from core.violations.base import ViolationResult
from core.violations.registry import register

@dataclass
class NoRecentImpressions:
    code: str = "no_recent_impressions_14d"
    description: str = "Enabled campaigns with zero impressions in the last 14 days"
    days: int = 14
    client: Any | None = None  # expects an object with execute_gaql()

    def _build_gaql(self, days: int) -> str:
        return f"""
          SELECT campaign.id, campaign.name, metrics.impressions
          FROM campaign
          WHERE campaign.status = 'ENABLED'
            AND segments.date DURING LAST_{days}_DAYS
          """.strip()

    def _rows_with_zero_impr(self, rows: Iterable[dict]) -> list[dict]:
        out: list[dict] = []
        for r in rows:
            impr = r.get("impressions")
            try:
                impr_f = float(impr)
            except Exception:
                impr_f = 0.0 if impr in (None, "", 0) else 1.0
            if impr_f == 0.0:
                out.append({
                    "campaign_id": r.get("campaign_id") or r.get("campaign.id"),
                    "campaign_name": r.get("campaign_name") or r.get("campaign.name"),
                    "impressions": 0
                })
        return out

    def run(self, customer_id: str, **params) -> ViolationResult:
        days = int(params.get("days", self.days))
        gaql = self._build_gaql(days)

        entities: list[dict] = []
        if self.client and hasattr(self.client, "execute_gaql"):
            try:
                rows = list(self.client.execute_gaql(customer_id, gaql))
                entities = self._rows_with_zero_impr(rows)
            except Exception as e:
                return ViolationResult(False, {"entities": [], "meta": {"checked_days": days, "gaql": gaql, "adapter_error": str(e)}})
        violated = len(entities) > 0
        return ViolationResult(violated, {"entities": entities, "meta": {"checked_days": days, "gaql": gaql}})

register(NoRecentImpressions())
