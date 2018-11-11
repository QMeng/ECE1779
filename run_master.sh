#!/usr/bin/env bash
source venv/bin/activate
gunicorn -w 1 --worker-class gevent --access-logfile access.log --error-logfile error.log -b 0.0.0.0:8080 app_master:app_master