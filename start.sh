#!/bin/bash

cd /webapp1
git reset --hard HEAD
git pull
flask run --cert=/cert.pem --key=/key.pem --host 0.0.0.0 \
--log-driver=splunk \
--log-opt splunk-token=eyJraWQiOiJzcGx1bmsuc2VjcmV0IiwiYWxnIjoiSFM1MTIiLCJ2ZXIiOiJ2MiIsInR0eXAiOiJzdGF0aWMifQ.eyJpc3MiOiJtZmFueDIgZnJvbSBERUxMIiwic3ViIjoibWZhbngyIiwiYXVkIjoiRG9ja2VyIiwiaWRwIjoiU3BsdW5rIiwianRpIjoiMzU4MTJhMmEyMjZmNDM5YTU2NDFjNzMxZTMxZDBhM2E0MDU2MzQxZTkzYzU0NjJjOTNjMTlkMGJjODc4ZjgyNiIsImlhdCI6MTU3MjAxODEwNCwiZXhwIjowLCJuYnIiOjE1NzIwMTgxMDR9.QQp7keROdI7bUiMjQbvmam0AOHgW1zuE9s7TJS0yTbF0420FFqeE-rZ67kRIE1ljDZfOALJUbPqMy5hmGG6h9w \
--log-opt splunk-url=http://192.168.1.88:8000