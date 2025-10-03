# Repository and Deployment Guide

## Prerequisites
- You must be on the correct branch (or `main`) → `git status`
- All tests should pass locally → `pip install -r requirements.txt && PYTHONPATH=. pytest -q`

## 1. Build & Push
Build and push the image to Google Container Registry:
gcloud builds submit --config=cloudbuild.yaml .

## 2. Check the logs if there is an issue
Stream logs for a specific build:
gcloud builds log --stream BUILD_ID

Read the last 100 lines of Cloud Run logs:
gcloud run services logs read manager-monitor --region=australia-southeast2 --limit=100

## 3. Push branch to GitHub
git push -u origin YOUR_BRANCH

Or merge your branch into main and push:
git checkout main
git pull origin main
git merge YOUR_BRANCH -m "Merge YOUR_BRANCH into main"
git push origin main

## 4. Clean up branch
git branch -d YOUR_BRANCH
git push origin --delete YOUR_BRANCH

## 5. (Optional) Manual Deploy to Cloud Run
gcloud run deploy manager-monitor --image gcr.io/the-quantified-web-operations/manager-monitor --region=australia-southeast2
