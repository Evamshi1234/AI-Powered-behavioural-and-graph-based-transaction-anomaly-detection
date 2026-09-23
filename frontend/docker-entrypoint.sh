#!/bin/sh
set -e
API_UPSTREAM="${API_UPSTREAM:-http://api:8000}"
case "$API_UPSTREAM" in
  http://*|https://*) ;;
  *) API_UPSTREAM="https://${API_UPSTREAM}" ;;
esac
export API_UPSTREAM
envsubst '${API_UPSTREAM}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
exec nginx -g 'daemon off;'
