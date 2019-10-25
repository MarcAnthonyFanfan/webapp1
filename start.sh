#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
if [ "$HOSTNAME" = u1910-dev ]; then
    export FLASK_ENV=development
else
    export FLASK_ENV=production
fi
flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0