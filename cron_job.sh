#!/bin/bash

DIRECTORY=/home/ozeliurs/discord-bot

echo "Running cron job"

cd $DIRECTORY || exit

echo "Check if there is a new commit"
git fetch

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "Up-to-date"
    exit 0
fi

echo "Need to pull"
git pull

echo "Killing screen"
screen -X -S "server" quit

echo "Starting screen"
# Start screen with name "server", run the command python3 app.py and detach immediately
screen -dmS "server" python3 app.py

echo "Cron job complete"