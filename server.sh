#!/bin/bash

export PYTHONPATH=$(pwd)

if [[ "$OSTYPE" == "linux"* ]] || [[ "$OSTYPE" == "linux-android"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Starting server..."
    uvicorn api.server:app --reload

elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Starting server..."
    uvicorn api.server:app --reload

else
    echo "Please use one of the verified Operating Systems to start the server. Visit: https://github.com/AmethystMac/staking-deposit-server.git"
    exit 1

fi
