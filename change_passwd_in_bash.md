# Password Management with Bash Scripts
## 1. Using chpasswd (Recommended for Non-Interactive Password Changes)

The `chpasswd` command is designed for non-interactive password changes. It reads `username:password` pairs from standard input or a file.

### Example Script:

```bash
#!/bin/bash

# Set the username and new password
USERNAME="example_user"
NEW_PASSWORD="new_password123"

# Change the password using chpasswd
echo "$USERNAME:$NEW_PASSWORD" | sudo chpasswd

echo "Password for $USERNAME has been changed."
```

### Key Points:
- **Security Note:** Avoid hardcoding passwords in scripts. Use environment variables or secure input methods instead.
- **Permissions:** The script must be run with `sudo` or as the root user because `chpasswd` requires elevated privileges.

## 2. Using passwd with stdin (Not Recommended for Security Reasons)

You can use the `passwd` command with input redirection, but this method is not recommended because it exposes the password in the command history or process list.

### Example Script:

```bash
#!/bin/bash

# Set the username and new password
USERNAME="example_user"
NEW_PASSWORD="new_password123"

# Change the password using passwd
echo -e "$NEW_PASSWORD\n$NEW_PASSWORD" | sudo passwd "$USERNAME"

echo "Password for $USERNAME has been changed."
```

### Key Points:
- **Security Risk:** The password is visible in the script and command history.
- **Permissions:** Requires `sudo` or root privileges.

## 3. Using expect for Interactive Automation

The `expect` command can automate interactive programs like `passwd`. It waits for specific prompts and sends responses automatically.

### Example Script:

```bash
#!/bin/bash

# Set the username and new password
USERNAME="example_user"
NEW_PASSWORD="new_password123"

# Use expect to automate the passwd command
expect << EOF
spawn passwd $USERNAME
expect "New password:"
send "$NEW_PASSWORD\r"
expect "Retype new password:"
send "$NEW_PASSWORD\r"
expect eof
EOF

echo "Password for $USERNAME has been changed."
```

### Key Points:
- **Security Note:** Avoid hardcoding passwords in scripts. Use secure input methods.
- **Dependency:** Requires the `expect` package to be installed (`sudo apt install expect` on Debian-based systems).
- **Permissions:** Requires `sudo` or root privileges.

## 4. Using openssl to Generate Encrypted Passwords

You can generate an encrypted password using `openssl` and then use `usermod` or `chpasswd` to set it.

### Example Script:

```bash
#!/bin/bash

# Set the username and new password
USERNAME="example_user"
NEW_PASSWORD="new_password123"

# Generate an encrypted password
ENCRYPTED_PASSWORD=$(openssl passwd -1 "$NEW_PASSWORD")

# Change the password using usermod
sudo usermod --password "$ENCRYPTED_PASSWORD" "$USERNAME"

echo "Password for $USERNAME has been changed."
```

### Key Points:
- **Security Note:** Avoid hardcoding passwords in scripts.
- **Permissions:** Requires `sudo` or root privileges.

## 5. Using read to Securely Input Passwords

To avoid hardcoding passwords in the script, you can use the `read` command to securely input the password during script execution.

### Example Script:

```bash
#!/bin/bash

# Prompt for the username
read -p "Enter username: " USERNAME

# Securely prompt for the new password
read -s -p "Enter new password: " NEW_PASSWORD
echo
read -s -p "Retype new password: " NEW_PASSWORD_CONFIRM
echo

# Check if passwords match
if [ "$NEW_PASSWORD" != "$NEW_PASSWORD_CONFIRM" ]; then
    echo "Passwords do not match. Exiting."
    exit 1
fi

# Change the password using chpasswd
echo "$USERNAME:$NEW_PASSWORD" | sudo chpasswd

echo "Password for $USERNAME has been changed."
```

### Key Points:
- **Security:** Passwords are not hardcoded and are securely input during script execution.
- **Permissions:** Requires `sudo` or root privileges.

## Best Practices:
- **Avoid Hardcoding Passwords:** Never hardcode passwords in scripts. Use secure input methods or environment variables.
- **Use chpasswd or usermod:** These commands are designed for non-interactive password changes and are safer than using `passwd` with stdin.
- **Run as Root:** Password changes require elevated privileges, so ensure the script is run with `sudo` or as the root user.
- **Test in a Safe Environment:** Always test scripts in a non-production environment before deploying them.

### Example of a Secure Script:

Here’s a secure script that uses `read` to input the password and `chpasswd` to change it:

```bash
#!/bin/bash

# Prompt for the username
read -p "Enter username: " USERNAME

# Securely prompt for the new password
read -s -p "Enter new password: " NEW_PASSWORD
echo
read -s -p "Retype new password: " NEW_PASSWORD_CONFIRM
echo

# Check if passwords match
if [ "$NEW_PASSWORD" != "$NEW_PASSWORD_CONFIRM" ]; then
    echo "Passwords do not match. Exiting."
    exit 1
fi

# Change the password using chpasswd
echo "$USERNAME:$NEW_PASSWORD" | sudo chpasswd

echo "Password for $USERNAME has been changed."
```
