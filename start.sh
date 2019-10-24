#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
flask run --cert=adhoc --host 0.0.0.0