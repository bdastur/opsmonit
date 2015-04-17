#!/bin/bash

set -e

# Set ENV Variables Needed by opsmonit.

# openrc credentials information 
: ${ADMIN_USER:=admin}
: ${ADMIN_USER_PASSWORD:=password}
: ${ADMIN_TENANT_NAME:=admin}

echo "Ops Monit Start"

exec /dockers/monit/monit.py

