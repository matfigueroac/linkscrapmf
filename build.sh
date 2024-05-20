#!/bin/bash
# Install Chrome
apt-get update
apt-get install -y wget unzip
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/