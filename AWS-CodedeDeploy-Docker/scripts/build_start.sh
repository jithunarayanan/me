#!/bin/bash
if docker images | grep -q 'jithu'; then
    docker image rm jithu
	cd /home/ubuntu/myapp && docker-compose up -d
else
	cd /home/ubuntu/myapp && docker-compose up -d
fi
