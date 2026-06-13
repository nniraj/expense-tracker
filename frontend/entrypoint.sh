#!/bin/sh
set -e

# Copy the custom nginx config
cp /app/nginx.conf /etc/nginx/conf.d/default.conf

# Start nginx
exec nginx -g "daemon off;"
