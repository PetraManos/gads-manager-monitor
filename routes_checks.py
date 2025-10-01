from fastapi import APIRouter, HTTPException
from core.gads import AdsProvider, make_client
from core.checks.registry import registry

# Import examples so they self-register
from core.checks.examples import has_campaigns  # noqa: F401

router = APIRouter(prefix="/checks", tags=["checks"])

@router.get("/")
def list_checks():
    return [{"code": c, "description": registry.get(c).description} for c in registry.list()]

@router.get("/run")
def run_check(code: str, customer_id: str):
    chk = registry.get(code)
    if not chk:
        raise HTTPException(status_code=404, detail=f"Unknown check '{code}'")
    provider = AdsProvider(make_client())
    res = chk.run(provider, customer_id)
    return res.__dict__
