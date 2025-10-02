from fastapi import FastAPI, Body, HTTPException

# Routers present in your tree
from routes_checks import router as checks_router
from routers.violations import violations_router, set_provider

import os
from importlib.metadata import version as _pkg_version
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Ensure example checks register themselves on import
import core.checks.examples  # noqa: F401

# Only symbol that exists in core/checks/base.py
from core.checks.base import list_codes

# Core utilities from your core/ package (no core_shared.py)
from core.text import norm, make_key
from core.names import declared_type, expected_label
from core.dates import ymd, range_last_n_days
from core.numeric import as_number, parse_money_cell, parse_percent_cell

app = FastAPI()

# Mount routers from your codebase
app.include_router(checks_router)         # -> /checks (GET /, GET /run)
app.include_router(violations_router)     # -> /violations


# --- Google Ads helpers -------------------------------------------------------
def make_client():
    """Build a Google Ads client from env vars expected in Cloud Run."""
    cfg = {
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "login_customer_id": os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],  # digits only
        "client_id": os.environ["GOOGLE_ADS_OAUTH_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_OAUTH_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(cfg)


@app.on_event("startup")
def _inject_provider_if_possible():
    """Try to inject a Google Ads client into violations checks at startup.

    If env vars aren't present (e.g., local dev without creds), we just skip.
    """
    try:
        client = make_client()
        set_provider(client)
        print("[app] Injected Google Ads client into violations checks.", flush=True)
    except Exception as e:
        print(f"[app] Skipping provider injection (env/creds missing?): {e}", flush=True)


# --- Basic health/info routes -------------------------------------------------
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
        rows = svc.search(
            customer_id=os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],
            query=q,
        )
        return [{"id": r.customer.id, "name": r.customer.descriptive_name} for r in rows]
    except GoogleAdsException as e:
        detail = {
            "request_id": e.request_id,
            "failure": [f"{err.error_code}: {err.message}" for err in e.failure.errors],
        }
        raise HTTPException(status_code=502, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Core helpers self-test (no Google Ads calls) -----------------------------
@app.get("/core/selftest")
def core_selftest():
    return {
        "norm(' Foo\\u00A0  Bar  ')"          : norm(" Foo\u00A0  Bar  "),
        "make_key"                            : make_key("Acme  Co", " CODE-123 "),
        "ymd"                                 : ymd(),
        "range_7_days"                        : range_last_n_days(7),
        "as_number_5pct"                      : as_number("5%"),
        "as_number_0.05"                      : as_number("0.05"),
        "money_$1,234.56"                     : parse_money_cell("$1,234.56"),
        "percent_'0.5'"                       : parse_percent_cell("0.5"),
        "declared_type('Brand - Phrase')"     : declared_type("Brand - Phrase"),
        "expected_label(PHRASE_ONLY)"         : expected_label("PHRASE_ONLY"),
        "checks_available"                    : list_codes(),
    }


# --- Temporary stub to avoid old broken import of run_checks ------------------
# Your checks API now lives in routes_checks.py (GET /checks, GET /checks/run).
# If any clients still POST to /checks/run, keep a stub to guide them.
@app.post("/checks/run")
def checks_run_stub(payload: dict = Body(default={})):
    return {
        "status": "moved",
        "use": "GET /checks/run?code=...&customer_id=...",
        "note": "The old POST /checks/run endpoint is no longer implemented here.",
    }
