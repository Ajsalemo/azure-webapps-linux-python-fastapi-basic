#!/bin/bash

echo "executing startup.sh from $(pwd)/startup.sh"

# uvicorn app:app --host '0.0.0.0'
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 -w 4 --threads 3 --timeout 600 --access-logfile '-' --error-logfile '-' app:app

