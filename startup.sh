#!/bin/bash

echo "executing startup.sh from $(pwd)/startup.sh"

apt-get install -yy freetds-dev gcc libkrb5-dev python3-dev openssl openssl-dev
pip install --ignore-installed --no-binary :all: pymssql

uvicorn app:app --host '0.0.0.0'
