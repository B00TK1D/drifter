#!/bin/sh
# Ensure apt is up to date
sudo apt update -y
# Install apt packages
sudo apt install -y python3 python3-pip gpsd gpsd-clients
# Install python packages
sudo pip3 install -r requirements.txt
# Modify service file
echo $(pwd)/app.py >>  driver.service
# Install service
sudo cp drifter.service /etc/systemd/system/drifter.service
sudo systemctl daemon-reload
sudo systemctl enable drifter.service
sudo systemctl start drifter.service