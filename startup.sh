#!/bin/bash
pip install -r requirements.txt
gunicorn app.main:app --bind=0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker