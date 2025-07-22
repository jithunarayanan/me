#!/bin/bash

# Replace with your Dynu username, password, and hostname
USERNAME="jithutnarayanan"
PASSWORD="ab50ecd39563106d4594593705e9b2a9"
HOSTNAME="jithu.gleeze.com"

# Get the current IP address
CURRENT_IP=$(curl -s ifconfig.me)

# Construct the Dynu update URL
UPDATE_URL="https://api.dynu.com/nic/update?hostname=$HOSTNAME&myip=$CURRENT_IP&username=$USERNAME&password=$PASSWORD"

# Update the IP address with Dynu
curl -s "$UPDATE_URL"

# Optional: Log the update (you can adjust the logging)
echo "$(date): Dynu update for $HOSTNAME to $CURRENT_IP" >> ./dynu.log