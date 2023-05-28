#!/bin/bash

cd ~/Network_Media/final/server

while :
do
    # start python server
    echo -e "Running server on 8000..."
    gunicorn server:app

    # check if server is on
    server=$(lsof -n -i | grep LISTEN)

    if [ "$server" != "" ]
    then
        break
    else
        sleep 5
    fi
done
