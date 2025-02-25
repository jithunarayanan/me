# **Mysql Replications**

### **Introduction**
MySQL replication is the process which a single data set, stored in a MySQL database, will be live-copied to a second server. This configuration, called master-slave replication, is a typical setup. The Other setup will be better because master-master replication allows data to be copied from either server to the other one. This setup allows us to perform MySQL reads or writes from either server. This configuration adds redundancy and increases efficiency when dealing with accessing the data.

The both setups is used for purticular workloads. In here we are looking both setups. The examples in this article will be based on two Ubuntu 20.04 VMs, named **Server A** and **Server B** and Using MySQL version 8.<br/>
**Server A: 172.31.1.1** <br/>
**Server B: 172.31.1.2**


### **Master-Slave Replication**
**Master Setup**<br/>
Install and Configure MySQL on Server A for a Master database. The first thing is to install MySQL-server on Server A by typing the following command.
```
sudo apt install mysql mysql-server
sudo service mysql start
sudo service mysql enable
sudo mysql_secuer_installation
```
Once the packages are properly installed, we need to configure Server A, for that, we need to start by editing the /etc/mysql/mysql.conf.d/mysqld.cnf file.
```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```
```
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = example
bind-address = 172.31.1.1
```
The first of those lines to identify our particular server, in our replication configuration uniquely. The second line indicates the file in which changes to any MySQL database or table will be logged. The third line indicates which databases we want to replicate between our servers. We can add as many databases to this line as we like. When we comment on this line, all the databases will replicate. And the last line tells our server to accept connections from the internet.

Remember that you're turning your other MySQL instance into a replica of this one, so the replica must be able to read whatever new data gets written to the source installation. To allow this, you must configure your source MySQL instance to listen for connections on an IP address that the replica will be able to reach, such as the source server's public IP address.

>Note: If you want to replicate more than one database, you can add another binlog_do_db directive for every database you want to add. This tutorial will continue with replicating only a single database, but if you want to replicate more it might look like this,
```
binlog_do_db = db
binlog_do_db = db_1
binlog_do_db = db_2
```
Alternatively, you can specify which databases MySQL should not replicate by adding a binlog_ignore_db directive for each one.
```
binlog_ignore_db = db_to_ignore
```
Now we need to restart MySQL.
```
sudo service mysql restart
```
Log in as the root user.
```
mysql -u root -p
```
Once we are logged in, We need to create a replication user that will be used for replicating data to Servers B.
```
mysql> CREATE USER 'replica_user'@'replica_server_ip' IDENTIFIED WITH mysql_native_password BY 'password';
```
From the prompt, create a new MySQL user. The following example will create a user named replica_user, but you can name yours whatever you'd like. Be sure to change replica_server_ip to your replica server's public IP address.

>**Note:** This command specifies that replica_user will use the mysql_native_password authentication plugin. It's possible to instead use MySQL's default authentication mechanism, caching_sha2_password, but this would require setting up an encrypted connection between the source and the replica.

Next, we need to give this user permissions to replicate our MySQL data:
```
mysql> GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'replica_server_ip';
mysql> FLUSH PRIVILEGES;
```
We need to make a note of the file and position which will be used in the next step. The following command will output the important pieces of information.

```
+------------------+----------+--------------+-----------------+
| File             | Position | Binlog_Do_DB |Binlog_Ignore_DB |
+------------------+----------+--------------+-----------------+
| mysql-bin.000001 |      107 | example      |                 | 
+------------------+----------+--------------+-----------------+
1 row in set (0.00 sec)
```

**Slave setup**<br/>
Install and Configure MySQL-server on Server B for a replica. We need to repeat the same steps that we followed on Server A.
```
sudo apt install mysql-server
sudo service mysql srtart
sudo service mysql enable
sudo mysql_secure_installation
```
Once the packages are properly installed, we need to configure it in much the same way as we configured Server A. We will start by editing the /etc/mysql/mysql.conf.d/mysqld.cnf file. We need to change the same four lines in the configuration file as we changed earlier. The defaults are listed below, followed by the changes we need to make.

```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 127.0.0.1
server-id = 2
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = example
relay-log = /var/log/mysql/mysql-relay-bin.log
```
Following that, update the log_bin and binlog_do_db values so that they align with the values you set in the source machine's configuration file. Lastly, add a relay-log directive defining the location of the replica's relay log file. Include the following line at the end of the configuration file. After saving and quitting that file, we need to restart the MySQL service.
```
sudo service mysql restart
```
Login to Server B as the root user,
```
mysql -u root -p
```
To start replicating data from the source, open up the MySQL shell on the replica server,

```
mysql> STOP REPLICA;

mysql> CHANGE REPLICATION SOURCE TO SOURCE_HOST='172.31.1.1',
SOURCE_USER='replica_user',
SOURCE_PASSWORD='password',
SOURCE_LOG_FILE='mysql-bin.000001',
SOURCE_LOG_POS=107;

mysql> START REPLICA;
```
After running this command, once you enable replication on this instance it will try to connect to the IP address following SOURCE_HOST using the username and password following SOURCE_USER and SOURCE_PASSWORD, respectively. It will also look for a binary log file with the name following SOURCE_LOG_FILE and begin reading it from the position after SOURCE_LOG_POS. We will check the replica's current state by running with the following show replica command. The \G modifier in this command rearranges the text to make it more readable.
```
SHOW REPLICA STATUS\G;
```
This command returns a lot of information that can be helpful when troubleshooting:
```
*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: 172.31.1.1
                  Master_User: replica_user
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 107
               Relay_Log_File: CMSAPP2-relay-bin.000001
                Relay_Log_Pos: 602
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes

```
Make sure Slave_IO_State is in *Waiting for source to send event* and Slave_IO_Running and Slave_SQL_Running are *yes.

**Troubleshooting**<br/>
If your replica has an issue in connecting or replication stops unexpectedly, it may be that an event in the source's binary log file is preventing replication. In such cases, you could run the SET GLOBAL SQL_SLAVE_SKIP_COUNTER command to skip a certain number of events following the binary log file position you defined in the previous command. This example only skips the first event:
```
mysql> STOP REPLICA;
mysql> SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;
```
Following that, you'd need to start the replica again:
```
mysql> START REPLICA;
```


### **Multi-Master Replication**
The examples in this article will be based on two Ubuntu 20.04 VMs, named **Server A** and **Server B** and Using MySQL version 8.

**Server A: 10.10.1.1** <br/>
**Server B: 10.10.1.2**
### **Prerequisite**
- VPN access
- Two ubuntu 20.04 machines

### **Steps**

**1st Master setup**<br/>
Install and Configure MySQL-server on **Server A**

The first thing to install, start and enable the MySQL-server on Server A by typing the following commands.
```
sudo apt install mysql-server
service mysql start
service mysql enable
mysql_secure_installation
```
Once the packages are properly installed, we need to configure Server A. To change the default behaviour for replication. We need to edit the config file on Server A. There are some lines that we need to change, which are currently set to the following,
```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```
```
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = example
# bind-address = 127.0.0.1
```

The first of those lines is to identify our particular server, in our replication configuration uniquely. The second line indicates the file in which changes to any MySQL database or table will be logged. The third line indicates which databases we want to replicate between our servers. You can add as many databases to this line as you'd like. When we comment the line all the databases in the server are replicated. The article will use a single database named "example" for simplicity. And the last line tells our server to accept connections from the internet (by not listening on 127.0.0.1).

Now we need to restart the MySQL service.
```
sudo service mysql restart
```
Then Login root user with the password
```
mysql -u root -p
```
Once we are logged in, We need to create a user that will be used for replicating data between our two Servers.
```
mysql> CREATE USER 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
```
Next, we need to give permission for this user  to replicate our MySQL data.
```
mysql> GRANT REPLICATION on *.* TO 'replica_user'@'%';
mysql> FLUSH PRIVILEGES;
```

Before the next step, we need to get some information about the current MySQL instance which we will later provide to Server B. The following command will output a few pieces of important information, which we will need to make note of.
```
mysql> SHOW MASTER STATUS;
```
The output will look like the following and will have two pieces of critical information, File and Position.
```
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000001 |    107   | example      |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.00 sec)
```
We need to make a note of the file and position which will be used in the next step.

**2nd Master setup**<br/>
Install and Configure MySQL-server on **Server B**. 

We need to repeat the same steps that we followed on Server A.
```
sudo apt install mysql-server
sudo service mysql start
sudo service mysql enable
mysql_secure_installation
```
Once the packages are properly installed, we need to configure it in much the same way as we configured Server A. We will start by editing the /etc/mysql/mysql.conf.d/mysqld.cnf file. We need to change the same four lines in the configuration file as we changed earlier. The defaults are listed below, followed by the changes we need to make.

```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```
```
server-id = 2
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = example
# bind-address = 127.0.0.1
```
We need to change these four lines to match the lines below. Please note that, unlike Server A, the server-id for Server B cannot be set to 1, In this server, it is 2. After saving and quitting that file, need to restart the MySQL service.
```
sudo service mysql restart
```
Login to Server B as the root user,
```
mysql -u root -p
```
First, just as on Server B, we are going to create the user who will be responsible for the replication.
```
mysql> CREATE USER 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
```
Next, we need to create the database that we are going to replicate across both servers.
```
mysql> CREATE DATABASE example;
```
And we need to give our newly created 'replica_user' user permissions to replicate it.
```
mysql> GRANT REPLICATION on *.* to 'replica_user'@'%';
mysql> FLUSH PRIVILEGES;
```
The next step involves taking the information that we took note of earlier which is MASTER_LOG_FILE and MASTER_LOG_POSITION to apply it to our MySQL server. This will allow replication to begin. The following commands should be able to do that.
```
mysql> STOP SLAVE ;
mysql> CHANGE MASTER TO MASTER_HOST = '10.10.1.1', MASTER_USER = 'replica_user', MASTER_PASSWORD = 'password', MASTER_LOG_FILE = 'mysql-bin.000001', MASTER_LOG_POS = 107;
mysql> START SLAVE;
```

We need to replace the values for MASTER_LOG_FILE and MASTER_LOG_POS may differ from those above. We should copy the values that "SHOW MASTER STATUS" returns on Server A. Then we need to check the slave status with show slave status command,
```
mysql> SHOW SLAVE STATUS\G;
```
The output will look similar to the following:
```
*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: 10.10.1.1
                  Master_User: replica_user
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 107
               Relay_Log_File: CMSAPP2-relay-bin.000005
                Relay_Log_Pos: 602
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
            
```

We must confirm that the *Slave_IO_State* is in *Waiting for source to send event* state and *Slave_IO_Running*, *Slave_SQL_Running* is in *Yes*. The last thing we have to do before we complete the MySQL master-master replication is to make note of the master log file and position to use to replicate in the other direction (from **Server B** to **Server A** ). We can do that by typing the following command in Server B.
```
mysql> SHOW MASTER STATUS;
```
The output will look similar to the following:
```
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000004 |      107 | example      |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.00 sec)
```
Take note of the file and position, as we will have to enter those on **Server B**, to complete the two-way replication.


**Complete Replication on Server A** <br/>
Back on Server A, we need to finish configuring replication on the command line. Running this command will replicate all data from Server B.
```
mysql> STOP REPLICA;
mysql> CHANGE MASTER TO MASTER_HOST = '10.10.1.2', MASTER_USER = 'replica_user', MASTER_PASSWORD = 'password', MASTER_LOG_FILE = 'mysql-bin.000004', MASTER_LOG_POS = 107;
mysql> START REPLICA;
```
Keep in mind that the values may differ from those above. The output will look similar to the following:
```
Query OK, 0 rows affected (0.01 sec)
```
Then we need to check the slave status with show slave status command,
```
mysql> SHOW SLAVE STATUS\G;
```
The output will look similar to the following:

```
*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: 10.10.1.2
                  Master_User: replica_user
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000004
          Read_Master_Log_Pos: 107
               Relay_Log_File: CMSAPP2-relay-bin.000005
                Relay_Log_Pos: 602
        Relay_Master_Log_File: mysql-bin.000004
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes

```
We must confirm that the *Slave_IO_State* is in *Waiting for source to send event* state and *Slave_IO_Running*, *Slave_SQL_Running* is in *Yes*.

**Troubleshooting**<br/>
If Slave_IO_Running: Yes Slave_SQL_Running: No, Check these commands.
```
mysql> STOP SLAVE;
mysql> SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;
mysql> START SLAVE;
```
If the start slave operation failed, check this command.
```
RESET SLAVE;
START SLAVE;
```
### **Outcome**
Successfully deployed MySQL Multi-Master and Master-Slave Replications.
