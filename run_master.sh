#!/usr/bin/env bash
./venv/bin/gunicorn -w 1 --worker-class gevent --access-logfile access.log --error-logfile error.log -b 0.0.0.0:8080 app_master:app_master