# remote-chromedriver
a remote chromedriver in a docker container

# rpi/debian:buster
A simple docker debian image from debian/buster but with the raspberry pi repositories

Base for a quicker remote-chromedriver

Build the rootfs on a raspberry pi with the script build-rootfs.sh

Then the docker image

# rpi/remote-chromedriver:74.0.3729.157
Note that the headless mode does not work with the chromedriver and chromium provided in these repositories
It still quicker for an unknow reason

Use chromium version 74.0.3729.157  instead of the debian buster one (76.0.3809.100)
And the name package slightly change:
  
chromium  become       chromium-browser
  
chromium-l10n become chromium-browser-l10n

chromium-driver become  chromium-driver

chromium-sandbox does not exist
