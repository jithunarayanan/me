
# DDNS Auto Update Script (Dynu)

This SOP describes how to use the following Bash script to automatically update your Dynu DNS record with your current public IP address. This is useful for machines with dynamic IPs, such as home servers or cloud instances.

## Script Details

```bash
#!/bin/bash

# Replace with your Dynu username, MD5-hashed password, and hostname
USERNAME="jithutnarayanan"
PASSWORD="ab50ecd39563106d4594593705e9b2a9"  # This should be your Dynu password hashed with MD5
HOSTNAME="jithu.gleeze.com"

# Get the current IP address
CURRENT_IP=$(curl -s ifconfig.me)

# Construct the Dynu update URL
UPDATE_URL="https://api.dynu.com/nic/update?hostname=$HOSTNAME&myip=$CURRENT_IP&username=$USERNAME&password=$PASSWORD"

# Update the IP address with Dynu
curl -s "$UPDATE_URL"

# Optional: Log the update (you can adjust the logging)
echo "$(date): Dynu update for $HOSTNAME to $CURRENT_IP" >> ./dynu.log
```

### Steps

1. **Edit the script**  
    Replace `USERNAME`, `PASSWORD`, and `HOSTNAME` with your Dynu account details.  
    **Note:** The `PASSWORD` variable should contain your Dynu password hashed with MD5.

2. **Save the script**  
    Save the script to a file, e.g., `ddns-auto-update.sh`.

3. **Make the script executable**  
    ```bash
    chmod +x ddns-auto-update.sh
    ```

4. **Test the script**  
    Run manually to verify:
    ```bash
    ./ddns-auto-update.sh
    ```

## Setting Up Cron Job

To update the IP every 5 minutes, add the following line to your crontab:

```cron
*/5 * * * * /Users/jithu/Desktop/me/ddns-auto-update.sh
```

Edit your crontab with:
```bash
crontab -e
```

**Note:**  
On AWS EC2 instances, cron jobs only need to run when the machine is started, depending on the instance configuration and OS settings. The `@reboot` directive can be used in the cron job. Ensure the cron daemon is running and enabled for your user.

## Logging

The script appends update logs to `./dynu.log` in the same directory.

## Security

- Store your credentials securely.
- Restrict permissions on the script file.
- Use MD5-hashed passwords as required by Dynu for API authentication.