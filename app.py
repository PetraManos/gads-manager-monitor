from fastapi import FastAPI
from routers.violations import violations_router, set_provider
import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from importlib.metadata import version as _pkg_version
from core.checks.base import list_codes, run_checks
import core.checks.examples  # noqa: F401 ensure checks are registered


app = FastAPI()
# Mount violations endpoints
app.include_router(violations_router)

def make_client():
    cfg = {
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "login_customer_id": os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],  # digits only
        "client_id": os.environ["GOOGLE_ADS_OAUTH_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_OAUTH_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(cfg)

@app.get("/")
def root():
    return {"ok": True, "service": "manager-monitor"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/diag")
def diag():
    return {
        "google_ads_version": _pkg_version("google-ads"),
        "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        "has_dev_token": bool(os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")),
        "has_refresh_token": bool(os.environ.get("GOOGLE_ADS_REFRESH_TOKEN")),
    }

@app.get("/accessible")
def accessible():
    try:
        client = make_client()
        cs = client.get_service("CustomerService")
        res = cs.list_accessible_customers()
        return {"resource_names": list(res.resource_names)}
    except GoogleAdsException as e:
        detail = {
            "request_id": e.request_id,
            "failure": [f"{err.error_code}: {err.message}" for err in e.failure.errors],
        }
        raise HTTPException(status_code=502, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gaql/customers")
def list_customers():
    try:
        client = make_client()
        svc = client.get_service("GoogleAdsService")
        q = "SELECT customer.id, customer.descriptive_name FROM customer LIMIT 10"
        rows = svc.search(customer_id=os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"], query=q)
        return [{"id": r.customer.id, "name": r.customer.descriptive_name} for r in rows]
    except GoogleAdsException as e:
        detail = {
            "request_id": e.request_id,
            "failure": [f"{err.error_code}: {err.message}" for err in e.failure.errors],
        }
        raise HTTPException(status_code=502, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- core helpers self-test (doesn't touch Google Ads) ---
from core_shared import (
    norm, make_key, ymd, range_last_n_days, as_number,
    parse_money_cell, parse_percent_cell, declared_type, expected_label
)

@app.get("/core/selftest")
def core_selftest():
    return {
        "norm(' Foo\\u00A0 Bar  ')" : norm(" Foo\u00A0  Bar  "),
        "make_key"                 : make_key("Acme  Co", " CODE-123 "),
        "ymd_ADELAIDE"             : ymd(tz="Australia/Adelaide"),
        "range_7_days_ADELAIDE"    : range_last_n_days(7, tz="Australia/Adelaide"),
        "as_number_5pct"           : as_number("5%"),
        "as_number_0.05"           : as_number("0.05"),
        "money_$1,234.56"          : parse_money_cell("$1,234.56"),
        "percent_'0.5'"            : parse_percent_cell("0.5"),   # returns 50 (percent)
        "declared_type('Brand - Phrase')" : declared_type("Brand - Phrase"),
        "expected_label(PHRASE_ONLY)"     : expected_label("PHRASE_ONLY"),
    }


from fastapi import Body
# --- Checks API ---
@app.get("/checks")
def checks_catalog():
    return {"checks": list_codes()}

@app.post("/checks/run")
def checks_run(
    payload: dict = Body(..., example={
        "customers": [],                       # optional; defaults to LOGIN_CUSTOMER_ID
        "checks": ["no_enabled_campaigns"]     # which checks to run
    })
):
    client = make_ads_client()
    customers = payload.get("customers") or [os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"]]
    codes = payload.get("checks")
    out = []
    for cid in customers:
        out.extend(run_checks(client, str(cid), codes))
    return {"count": len(out), "violations": out}
