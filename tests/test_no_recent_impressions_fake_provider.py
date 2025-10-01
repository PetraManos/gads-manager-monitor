from core.violations.registry import registry
from routers.violations import set_provider

class FakeProvider:
    def execute_gaql(self, customer_id, query):
        # one zero, one non-zero; also exercise flexible keys for campaign fields
        return [
            {"campaign.id": "111", "campaign.name": "C1", "impressions": 0},
            {"campaign_id": "222", "campaign_name": "C2", "impressions": 42},
        ]

def test_no_recent_impressions_flags_zero_rows():
    set_provider(FakeProvider())
    chk = registry.get("no_recent_impressions_14d")
    res = chk.run("123-456-7890", days=14)
    assert res.violated is True
    assert isinstance(res.details, dict)
    ents = res.details["entities"]
    assert len(ents) == 1
    assert ents[0]["campaign_id"] == "111"
    assert ents[0]["impressions"] == 0
    assert "LAST_14_DAYS" in res.details["meta"]["gaql"]
