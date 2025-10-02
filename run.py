import os, importlib, sys

# Respect Cloud Run PORT
PORT = int(os.environ.get("PORT", "8080"))

# Candidate module paths to try, in order
CANDIDATES = [
    "manager_monitor.main:app",
    "manager_monitor.app:app",
    "manager_monitor.server:app",
    "app:app",
    "main:app",
    "server:app",
    "src.manager_monitor.main:app",
    "src.app:app",
]

def resolve_app(spec: str):
    """
    Given 'pkg.module:attr', import module and return getattr(module, attr)
    """
    mod_name, _, attr = spec.partition(":")
    if not attr:
        raise ValueError(f"Invalid spec (missing :app): {spec}")
    mod = importlib.import_module(mod_name)
    return getattr(mod, attr)

last_err = None
for spec in CANDIDATES:
    try:
        application = resolve_app(spec)
        print(f"[run.py] Using ASGI app: {spec}", flush=True)
        import uvicorn
        uvicorn.run(application, host="0.0.0.0", port=PORT)
        sys.exit(0)
    except Exception as e:
        last_err = e

print("[run.py] Failed to locate an ASGI app. Tried:", *CANDIDATES, sep="\n  ")
print(f"[run.py] Last error: {type(last_err).__name__}: {last_err}")
sys.exit(1)
