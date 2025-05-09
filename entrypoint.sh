#!/bin/bash

# uvicorn app:app --host '0.0.0.0' --workers 5
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 -w 4 --timeout 600 --access-logfile '-' --error-logfile '-' app:app
