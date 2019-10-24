#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0