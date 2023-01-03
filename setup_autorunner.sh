#!/bin/bash
sudo cp rocketrun.service /etc/systemd/system/rocketrun.service
sudo systemctl daemon-reload
sudo systemctl start rocketrun.service
sudo systemctl enable rocketrun.service