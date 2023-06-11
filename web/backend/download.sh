#!/bin/bash

device="${1:-mac_arm64}"

if [ "$device" != "mac_arm64" ] && [ "$device" != "mac64" ] && [ "$device" != "linux64" ] && [ "$device" != "win32" ]; then
    echo "Invalid device. Please choose from mac_arm64, mac64, linux64, win32"
    exit 1
fi

cd IOTA_crawler
echo "Downloading chromedriver for ${device}..."
wget "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_${device}.zip" > /dev/null 2>&1

echo "Unzipping chromedriver for ${device}..."
unzip "chromedriver_${device}.zip" > /dev/null 2>&1
rm "chromedriver_${device}.zip"
cd ..

echo "Installing required python packages..."
pip install -r requirements.txt > /dev/null 2>&1
