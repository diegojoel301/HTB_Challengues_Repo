#!/bin/ash

# Secure entrypoint
chmod 600 /entrypoint.sh

# Populate admin and session secret env
echo "ADMIN_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)" >> /app/.env
echo "SESSION_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)" >> /app/.env

/usr/bin/supervisord -c /etc/supervisord.conf