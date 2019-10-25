#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
HOSTNAME=$(hostname)
if [ "$HOSTNAME" = "u1910-dev" ]; then
    FLASK_ENV=development flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0
else
    FLASK_ENV=production flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0
fi