#!/bin/bash

python3 server.py

# check if server is on
server=$(lsof -n -i | grep LISTEN)

if [ "$server" != "" ]
then
    kill $(lsof -t -i:5000)
    echo -e "kill server running on 5000"
else
    echo "No server running on 5000"
fi