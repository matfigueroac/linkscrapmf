#!/bin/sh
set -e

# Install ChromeDriver
if [ ! -f /usr/local/bin/chromedriver ]; then
  wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
  unzip /tmp/chromedriver.zip -d /usr/local/bin/
  rm /tmp/chromedriver.zip
fi

# Ensure ChromeDriver is executable
chmod +x /usr/local/bin/chromedriver

# Export the ChromeDriver path as an environment variable
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
