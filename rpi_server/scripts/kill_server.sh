#!/bin/bash

# check if server is on
server=$(lsof -n -i | grep LISTEN)

if [ "$server" != "" ]
then
    kill $(lsof -t -i:8000)
    echo -e "kill server running on 8000"
else
    echo "No server running on 8000"
fi
