#!/bin/bash -ex
mongod --bind_ip_all &
sleep 5
uvicorn app.main:app --host 0.0.0.0 --port 8080
