#!/bin/bash
sudo apt update
sudo apt upgrade
sudo apt-get install docker docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
systemctl start docker.service
systemctl enable docker.service
