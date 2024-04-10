#!/bin/bash

echo "Install packages"
apt install python3-flask
apt install python3-validators
apt install python3-torch
apt install python3-torchvision
apt install python3-edge
apt install python3-flask-cors

echo "Create directory"
mkdir ../static

echo "My IP address is: $(hostname -I | cut -d' ' -f1)"

echo "Run edge"
python3 main.py
