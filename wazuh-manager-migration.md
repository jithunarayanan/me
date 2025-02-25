# Wazuh-manager-migration
**Backup your files**<br>
To avoid losing any configuration data or agent keys, we will stop the wazuh-manager service and make a copy of the directory where it lives. But first, lets check if we have enough space to create a copy of /var/ossec:

```
sudo du -h /var/ossec | tail -n1
sudo df -h /var
```
Now we copy all files to a separated backup directory:
```
sudo service wazuh-manager stop
sudo cp -rp /var/ossec /var/ossec_backup
```
Move ossec_backup directory to the new server. We can use sftp or rsync service for this operation.


**Install wazuh-manager server**

```
apt-get update
apt-get install curl
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --no-default-keyring --keyring gnupg-ring:/usr/
echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee -a /etc/apt/sources.list.d/wazuh.list
apt-get update
apt-get install wazuh-manager
systemctl daemon-reload 
systemctl enable wazuh-manager.service 
systemctl start wazuh-manager.service
systemctl status wazuh-manager
```
**Restore configuration**

Before restoring our previous settings please note that some configuration options have been deprecated or use a different syntax, what can cause the manager not to start properly. To avoid this, you can manually try to migrate your settings. Same thing happens with rules and decoders.

The first step is to stop the wazuh-manager service:
```
sudo systemctl stop wazuh-manager
```
Now we will restore the following files:


```
cp -p /var/ossec_backup/agentless/.passlist /var/ossec/agentless/
cp -p /var/ossec_backup/etc/client.keys /var/ossec/etc/
cp -p /var/ossec_backup/etc/ossec.conf /var/ossec/etc/ossec.conf.orig
cp -p /var/ossec_backup/etc/local_internal_options.conf /var/ossec/etc/local_internal_options.conf
cp -p /var/ossec_backup/etc/local_decoder.xml /var/ossec/etc/decoders/local_decoder.xml
cp -p /var/ossec_backup/etc/shared/agent.conf /var/ossec/etc/shared/default/agent.conf
cp -p /var/ossec_backup/rules/local_rules.xml /var/ossec/etc/rules/local_rules.xml
cp -p /var/ossec_backup/queue/rids/sender_counter /var/ossec/queue/rids/sender_counter
```

There have been some syntax changes, and new settings, incorporated to ossec.conf file. Please review this file manually in order to import parts of your previous configuration from ossec.conf.orig. In addition, if you have existing ossec clients, then you may need to enable receiving UDP on port 1514 by changing the following block in ossec.conf:

From:
```
<remote>
  <connection>secure</connection>
  <port>1514</port>
  <protocol>tcp</protocol>
```
To:
```
<remote>
  <connection>secure</connection>
  <port>1514</port>
  <protocol>tcp,udp</protocol>
```
Also note that the *agent.conf* file directory has now changed to */var/ossec/etc/shared/default.*
Optionally the following files can be restored to preserve alert log files and syscheck/rootcheck databases:

```
cp -rp /var/ossec_backup/logs/archives/* /var/ossec/logs/archives
cp -rp /var/ossec_backup/logs/alerts/* /var/ossec/logs/alerts
cp -rp /var/ossec_backup/queue/rootcheck/* /var/ossec/queue/rootcheck
cp -rp /var/ossec_backup/queue/syscheck/* /var/ossec/queue/syscheck
cp -rp /var/ossec_backup/queue/db/* /var/ossec/queue/db
cp -rp /var/ossec_backup/queue/agents-timestamp /var/ossec/queue/agents-timestamp
```

Finally we can start the services again. Please check /var/ossec/logs/ossec.log file to ensure there are no errors or warnings related to the settings migration.

```
sudo systemctl start wazuh-manager
```

### **Outcome**
The wazuh-manager server successfully migrated.
