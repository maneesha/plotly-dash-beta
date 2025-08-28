#!/bin/bash
source .venv/bin/activate
source .app_environ

BIND="$1"

DENV=${DEPLOY_ENV:-prod}
LOGLEVEL=${LOG_LEVEL:-info}

gunicorn app:server --bind $BIND --log-level $LOGLEVEL --error-logfile /var/log/plotly-dash-beta/${DENV}_error.log --access-logfile /var/log/plotly-dash-beta/${DENV}_access.log --capture-output --timeout 600
