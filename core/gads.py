import os
from google.ads.googleads.client import GoogleAdsClient

def make_client():
    return GoogleAdsClient.load_from_dict({
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "login_customer_id": os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],
        "client_id": os.environ["GOOGLE_ADS_OAUTH_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_OAUTH_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "use_proto_plus": True,
    })

class AdsProvider:
    def __init__(self, client=None):
        self.client = client or make_client()

    def gaql(self, customer_id: str, query: str):
        svc = self.client.get_service("GoogleAdsService")
        return svc.search(customer_id=str(customer_id), query=query)
