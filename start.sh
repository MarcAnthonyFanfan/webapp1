#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
python3 app.py