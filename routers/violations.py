from fastapi import APIRouter, HTTPException
from core.violations.registry import registry
# Import checks so they self-register
from core.violations.examples.no_recent_impressions import NoRecentImpressions  # noqa: F401
from core.violations.examples.disapproved_ads import DisapprovedAds  # noqa: F401

violations_router = APIRouter(prefix="/violations", tags=["violations"])
_provider = None

def set_provider(p):
    """Inject a Google Ads provider and propagate it to all registered checks."""
    global _provider
    _provider = p
    # propagate to existing check instances (avoid poking at private dict directly)
    try:
        for code in registry.list():
            chk = registry.get(code)
            if hasattr(chk, "client"):
                setattr(chk, "client", p)
    except Exception:
        # keep silent; router path will still inject on-demand
        pass

@violations_router.get("/checks")
def list_checks():
    return registry.list()

@violations_router.get("/run")
def run_check(customer_id: str, check: str, days: int | None = None):
    try:
        c = registry.get(check)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown check: {check}")
    if hasattr(c, "client") and _provider is not None:
        setattr(c, "client", _provider)
    params = {"days": days} if days is not None else {}
    result = c.run(customer_id, **params)
    return {"violated": result.violated, "details": result.details}
