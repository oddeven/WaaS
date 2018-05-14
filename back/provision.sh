#!/usr/bin/env bash

# Update package list and upgrade all packages
apt-get update
#apt-get -y upgrade

# install pip3
apt-get -y install python3-pip

pip3 install requests pyyaml
