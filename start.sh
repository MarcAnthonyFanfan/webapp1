#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
case $HOSTNAME in
  (u1910-dev) export FLASK_ENV=development;;
  (u1910-prod) export FLASK_ENV=production;;
esac
flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0