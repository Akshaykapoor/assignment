#!/bin/sh
echo "********Making the VM ready for installing packages********"

echo "********Installing pip git curl********"
sudo apt-get install -y python-pip git curl

echo "********Installing node********"
sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -

echo "********Installing nodejs v4.5.0********"
sudo apt-get install -y nodejs

sudo apt-get install -y build-essential

echo "********Insatlling nginx...********"
sudo apt-get install -y nginx

echo "********Cloning git repo of AkshayKapoor********"
git clone https://github.com/Akshaykapoor/assignment.git

# Cd into the dir to install npm modules locally
cd assignment

echo "********Installing npm packages locally for the directory...********"
npm install yargs
npm install nginx-conf
