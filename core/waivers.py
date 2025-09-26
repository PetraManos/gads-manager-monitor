from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from .text import norm_collapse, find_col_eq
from .dates import normalize_date, now

@dataclass
class WaiverRecord:
    ops_lead: Optional[str]
    approved_by: Optional[str]
    expires_on_epoch_ms: Optional[int]
    reason: Optional[str]

def build_waivers_index(values: List[List[Any]]) -> Dict[str, WaiverRecord]:
    """
    Build index from a waiver sheet 2D array (header + rows).
    Columns: Client Name | Violation Code | Process Violation Reason | Ops Lead | Approved By | Approval Expiration Date
    """
    if not values or len(values) < 2:
        return {}
    header = [str(h or "").strip().lower() for h in values[0]]

    def col(name: str) -> int:
        i = find_col_eq(header, name)
        if i == -1: raise ValueError(f'Missing column "{name}" in waiver sheet.')
        return i

    c_client  = col("client name")
    c_code    = col("violation code")
    c_reason  = col("process violation reason")
    c_ops     = col("ops lead")
    c_appr    = col("approved by")
    c_expire  = col("approval expiration date")

    idx: Dict[str, WaiverRecord] = {}
    for r in values[1:]:
        client = norm_collapse(r[c_client])
        code   = norm_collapse(r[c_code])
        if not client or not code:
            continue
        ops_lead = str(r[c_ops]) if r[c_ops] is not None else None
        approved = str(r[c_appr]) if r[c_appr] is not None else None

        expires  = None
        x = r[c_expire]
        if isinstance(x, datetime):
            expires = int(normalize_date(x).timestamp()*1000)
        elif isinstance(x, str) and x.strip():
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"):
                try:
                    d = datetime.strptime(x.strip(), fmt)
                    expires = int(normalize_date(d).timestamp()*1000)
                    break
                except Exception:
                    pass

        key = f"{client}|{code}"
        idx[key] = WaiverRecord(ops_lead=ops_lead, approved_by=approved, expires_on_epoch_ms=expires, reason=str(r[c_reason]) if r[c_reason] is not None else None)
    return idx

def get_waiver_status_from_index(waivers_index: Dict[str, WaiverRecord],
                                 client_name: str,
                                 violation_code: str,
                                 today_epoch_ms: Optional[int]=None) -> Dict[str, Any]:
    key = f"{norm_collapse(client_name)}|{norm_collapse(violation_code)}"
    rec = waivers_index.get(key)
    if not rec:
        return {"found": False, "isActive": False, "approvedBy": None, "expiresOn": None, "reason": None}

    today = datetime.fromtimestamp((today_epoch_ms or int(now().timestamp()*1000))/1000.0, tz=ZoneInfo("UTC"))
    today_norm = normalize_date(today).date()
    not_expired = (rec.expires_on_epoch_ms is not None and
                   today_norm <= datetime.fromtimestamp(rec.expires_on_epoch_ms/1000.0, tz=ZoneInfo("UTC")).date())
    return {
        "found": True,
        "isActive": bool(not_expired),
        "approvedBy": rec.approved_by,
        "expiresOn": rec.expires_on_epoch_ms,
        "reason": rec.reason,
    }
