#!/bin/bash

export PYTHONPATH=$(pwd)

if [[ "$OSTYPE" == "linux"* ]] || [[ "$OSTYPE" == "linux-android"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Starting server..."
    uvicorn api.server:app --reload

elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Starting server..."
    python ./api/server.py "$@"

else
    echo "Sorry, to run deposit-cli on" $(uname -s)", please see the trouble-shooting on https://github.com/ethereum/staking-deposit-cli"
    exit 1

fi
