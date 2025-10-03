import importlib
from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_app_imports_and_root_ok():
    app_module = importlib.import_module("app")
    app = getattr(app_module, "app")
    assert isinstance(app, FastAPI)

    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert body.get("service") == "manager-monitor"
