from typing import Iterable, Protocol, Any

class ClientProvider(Protocol):
    """Abstracts Google Ads access. Real implementation wraps GoogleAdsClient."""
    def execute_gaql(self, customer_id: str, query: str) -> Iterable[dict[str, Any]]:
        ...

class NotConfiguredProvider:
    def execute_gaql(self, customer_id: str, query: str):  # pragma: no cover
        raise RuntimeError("Google Ads client provider is not configured")
