from core.checks.examples.has_campaigns import HasCampaigns

class FakeProvider:
    def __init__(self, n):
        self.n = n
    def gaql(self, customer_id, query):
        return range(self.n)

def test_has_campaigns_true():
    r = HasCampaigns().run(FakeProvider(1), "123")
    assert r.ok is True
    assert "campaign" in r.summary.lower()

def test_has_campaigns_false():
    r = HasCampaigns().run(FakeProvider(0), "123")
    assert r.ok is False
    assert "no" in r.summary.lower()
