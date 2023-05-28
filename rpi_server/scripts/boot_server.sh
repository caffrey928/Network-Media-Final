#!/bin/bash

cd ~/Network_Media/final/server

for i in {1..5}; do
    # start python server
    echo -e "Running server on 8000..."
    python3 server.py &
    sleep 3

    # check if server is on
    server=$(lsof -n -i | grep LISTEN)

    if [ "$server" != "" ]
    then
        break
    else
        sleep 5
    fi
done
