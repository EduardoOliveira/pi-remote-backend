#!/bin/bash

#raspi-config nonint do_i2c 0
#apt install python3-pip
#pip3 install trilobot

ln -s $(pwd)/controller.service /etc/systemd/system/controller.service
ln -s $(pwd)/camera.service /etc/systemd/system/camera.service
ln -s $(pwd)/caddy.service /etc/systemd/system/caddy.service


systemctl daemon-reload

systemctl enable controller.service
systemctl restart controller.service

systemctl enable camera.service
systemctl restart camera.service

systemctl enable caddy.service
systemctl restart caddy.service
