#!/bin/bash

if [ -f ../.env ]; then
    export $(grep -v '^#' ../.env | grep -v '^$' | grep -v 'METABASE_PATH' | xargs)
    echo "Environment variables loaded"
else
    echo ".env file not found"
    exit 1
fi