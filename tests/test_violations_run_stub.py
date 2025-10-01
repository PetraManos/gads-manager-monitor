from routers.violations import run_check

def test_run_check_no_provider_schema():
    resp = run_check(customer_id="123-456-7890", check="no_recent_impressions_14d", days=14)
    assert "violated" in resp
    assert "details" in resp
    assert "entities" in resp["details"]
    assert "meta" in resp["details"]
    assert resp["details"]["meta"]["checked_days"] == 14
    assert "gaql" in resp["details"]["meta"]
