#!/bin/bash

export PYTHONPATH=$(pwd)

if [[ "$OSTYPE" == "linux"* ]] || [[ "$OSTYPE" == "linux-android"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Starting keystore generator app..."
    python3.12 ./lib/deposit.py "$@"

elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Starting keystore generator app..."
    python ./lib/deposit.py "$@"

else
    echo "Sorry, to run deposit on" $(uname -s)", please see the trouble-shooting on https://github.com/ethereum/staking-deposit-cli"
    exit 1

fi
