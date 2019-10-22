#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
flask run --host 0.0.0.0