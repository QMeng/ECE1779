#!/usr/bin/env bash
source venv/bin/activate
gunicorn -w 4 --worker-class gevent --access-logfile access.log --error-logfile error.log -b 0.0.0.0:80 app:app_worker