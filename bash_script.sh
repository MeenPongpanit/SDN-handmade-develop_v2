#!/bin/bash

git fetch --all
git reset --hard origin/master
git pull

cd frontend
pkill -9 python3
pkill -9 node
HOST=0.0.0.0 PORT=3000 npm run dev &
cd ..
python3 backend/src/main_web.py &
python3 backend/src/main.py && fg