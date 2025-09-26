# Manager Monitor — Runbook

## Overview
Containerised Python/FastAPI app on Cloud Run for replacing Apps Script process violations, with Google Ads API access.

---

## Cloud
- **Project:** the-quantified-web-operations
- **Region:** australia-southeast2
- **Cloud Run service:** manager-monitor
- **Service account:** sa-manager-monitor@the-quantified-web-operations.iam.gserviceaccount.com

## Google Ads
- **Login customer ID (prod):** 258-152-6537 (digits: 2581526537)
- **Test manager ID:** 923-822-1682 (digits: 9238221682)
- **OAuth scope:** https://www.googleapis.com/auth/adwords
- **Developer token:** stored in Secret Manager (name below)

## Secrets (Secret Manager) — names only
- GOOGLE_ADS_DEVELOPER_TOKEN
- GOOGLE_ADS_OAUTH_CLIENT_ID
- GOOGLE_ADS_OAUTH_CLIENT_SECRET
- GOOGLE_ADS_REFRESH_TOKEN
- GOOGLE_ADS_LOGIN_CUSTOMER_ID

> Cloud Run service account must have **roles/secretmanager.secretAccessor** for these.

## Endpoints
- `/` — service banner
- `/ping` — health probe
- `/diag` — shows `google_ads_version`, `login_customer_id`, and presence of tokens
- `/gaql/customers` — sample GAQL list of customers
- `/core/selftest` — core helper sanity checks

---

## Build & Deploy (Cloud Build → Cloud Run)
- **Config:** `cloudbuild.yaml` at repo root
- **Manual trigger:**
```bash
gcloud builds submit --project the-quantified-web-operations \
  --substitutions=_TAG=$(date +%Y%m%d-%H%M%S),_REGION=australia-southeast2


