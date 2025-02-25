# Creating a software RAID during the installation

Redundant Arrays of Independent Disks (RAID) devices are constructed
from multiple storage devices that are arranged to provide increased
performance and, in some configurations, greater fault tolerance.

A RAID device is created in one step and disks are added or removed as
necessary. You can configure one RAID partition for each physical disk
in your system, so that the number of disks available to the
installation program determines the levels of RAID device available. For
example, if your system has two hard drives, you cannot create a RAID 10
device, as it requires a minimum of three separate disks.

>**Note**

On 64-bit IBM Z, the storage subsystem uses RAID transparently. You do
not have to configure software RAID manually.

**Prerequisites**

-   You have selected two or more disks for installation before RAID
    configuration options are visible. Depending on the RAID type you
    want to create, at least two disks are required.

-   You have created a mount point. By configuring a mount point, you
    can configure the RAID device.

-   You have selected the **Custom** radio button on the **Installation
    Destination** window.

**Procedure**

1.  From the left pane of the **Manual Partitioning** window, select the
    required partition.

2.  Under the **Device(s)** section, click **Modify**. The **Configure
    Mount Point** dialog box opens.

3.  Select the disks that you want to include in the RAID device and
    click **Select**.

4.  Click the **Device Type** drop-down menu and select **RAID**.

5.  Click the **File System** drop-down menu and select your preferred
    file system type.

6.  Click the **RAID Level** drop-down menu and select your preferred
    level of RAID.

7.  Click **Update Settings** to save your changes.

8.  Click **Done** to apply the settings to return to the **Installation
    Summary** window.

## Creating a software RAID on an installed system

You can create a software Redundant Array of Independent Disks (RAID) on
an existing system using the mdadm utility.

**Prerequisites**

-   The ```mdadm``` package is installed.

-   Two or more partitions exist on your system. For detailed
    instruction, see [Creating a partition with
    parted](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/getting-started-with-partitions_managing-storage-devices#proc_creating-a-partition-with-parted_getting-started-with-partitions).

**Procedure**

1.  Create a RAID of two block devices, for example */dev/sda1* and */dev/sdc1*:
```
# mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/sda1 /dev/sdc1
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```

2.  Optional: Check the status of the RAID:
```
# mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Thu Oct 13 15:17:39 2022
        Raid Level : raid0
        Array Size : 18649600 (17.79 GiB 19.10 GB)
      Raid Devices : 2
     Total Devices : 2
       Persistence : Superblock is persistent

       Update Time : Thu Oct 13 15:17:39 2022
             State : clean
    Active Devices : 2
   Working Devices : 2
    Failed Devices : 0
     Spare Devices : 0
[...]
```
3.  Optional: Observe the detailed information about each device in the
    RAID:
```
# mdadm --examine /dev/sda1 /dev/sdc1
/dev/sda1:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x1000
     Array UUID : 77ddfb0a:41529b0e:f2c5cde1:1d72ce2c
           Name : 0
  Creation Time : Thu Oct 13 15:17:39 2022
     Raid Level : raid0
   Raid Devices : 2
[...]
```

4.  Create a file system on the RAID drive:

```
# mkfs -t xfs /dev/md0
```
Replace xfs with the file system that you chose to format the drive with.


5.  Create a mount point for RAID drive and mount it:
```
# mkdir /mnt/raid1
# mount /dev/md0 /mnt/raid1
```
Replace */mnt/raid1* with the mount point.
If you want that RHEL mounts the md0 RAID device automatically when the system boots, add an entry for your 
device to the ```/etc/fstab``` file:
```
/dev/md0 */mnt/raid1 xfs* defaults 0 0
```
 

## Configuring a RAID volume using the storage System Role (RHEL)

With the storage System Role, you can configure a RAID volume on RHEL
using Red Hat Ansible Automation Platform and Ansible-Core. Create an
Ansible playbook with the parameters to configure a RAID volume to suit
your requirements.

**Prerequisites**

-   The Ansible Core package is installed on the control machine.

-   You have the rhel-system-roles package installed on the system from
    which you want to run the playbook.

-   You have an inventory file detailing the systems on which you want
    to deploy a RAID volume using the storage System Role.

**Procedure**

1.  Create a new *playbook.yml* file with the following content:
```
---
- name: Configure the storage
  hosts: managed-node-01.example.com
  tasks:
  - name: Create a RAID on sdd, sde, sdf, and sdg
    include_role:
      name: rhel-system-roles.storage
    vars:
    storage_safe_mode: false
    storage_volumes:
      - name: data
        type: raid
        disks: [sdd, sde, sdf, sdg]
        raid_level: raid0
        raid_chunk_size: 32 KiB
        mount_point: /mnt/data
        state: present
```


**Warning**
Device names might change in certain circumstances, for example, when
you add a new disk to a system. Therefore, to prevent data loss, do
not use specific disk names in the playbook.

2.  Optional: Verify the playbook syntax:
```
# ansible-playbook --syntax-check playbook.yml
```
3.  Run the playbook:
```
# ansible-playbook -i inventory.file /path/to/file/playbook.yml
```
> */path/to/file/playbook.yml***

**ADDITIONAL RESOURCES**

-   The /usr/share/ansible/roles/rhel-system-roles.storage/README.md file

-   [Preparing a control node and managed nodes to use RHEL System
    Roles](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/automating_system_administration_by_using_rhel_system_roles/assembly_preparing-a-control-node-and-managed-nodes-to-use-rhel-system-roles_automating-system-administration-by-using-rhel-system-roles)

## Extending RAID

You can extend a RAID using the ```--grow``` option of the ```mdadm``` utility.

**Prerequisites**

-   Enough disk space.
-   The ``parted``` package is installed.

**Procedure**

1.  Extend RAID partitions. For more information, see [Resizing a
    partition with
    parted](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/getting-started-with-partitions_managing-storage-devices#proc_resizing-a-partition-with-parted_getting-started-with-partitions).

2.  Extend RAID to the maximum of the partition capacity:
```
# mdadm --grow --size=max /dev/md0
```
To set a specific size, write the value of the ```--size``` parameter in kB, for example ```--size=524228```.

3.  Increase the size of file system. For example, if the volume uses
    XFS and is mounted to */mnt/*, enter:
```
# xfs_growfs /mnt/
```

> \# xfs_growfs /mnt/

**ADDITIONAL RESOURCES**

-   The mdadm(8) man page
-   [Managing file
    systems](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_file_systems/index)

## Shrinking RAID

You can shrink RAID using the ```--grow`` option of the ```mdadm``` utility.

**Important**
The XFS file system does not support shrinking.

**Prerequisites**
-   The ```parted``` package is installed.

**Procedure**
1.  Shrink the file system. For more information, see [Managing file
    systems](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_file_systems/index).

2.  Decrease the RAID to the size, for example to *512 MB*:
```
# mdadm --grow --size=524228 /dev/md0
```
Write the \--size parameter in kB.

3.  Shrink the partition to the size you need.

**ADDITIONAL RESOURCES**

-   The mdadm(8) man page
-   [Resizing a partition with
    parted](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/getting-started-with-partitions_managing-storage-devices#proc_resizing-a-partition-with-parted_getting-started-with-partitions).

## Supported RAID conversions

It is possible to convert from one RAID level to another. For example,
you can convert from RAID5 to RAID10, but not from RAID10 to RAID5. The
following table describes the supported RAID conversions:

  -----------------------------------------------------------------------
  **Source        **Destination level**
  level**         
  --------------- -------------------------------------------------------
  RAID0           RAID4, RAID5, RAID10

  RAID1           RAID0, RAID5

  RAID4           RAID0, RAID5

  RAID5           RAID0, RAID1, RAID4, RAID6, RAID10

  RAID6           RAID5

  RAID10          RAID0
  
  -----------------------------------------------------------------------

>**Note**

Converting RAID 5 to RAID0 and RAID4 is only possible with
the ALGORITHM_PARITY_N layout.

**ADDITIONAL RESOURCES.**

-   The mdadm(8) man page

## Converting a RAID level

You can convert RAID to a different RAID level as required. The
following example converts the RAID device /dev/md0 with level 0 to 5
and add one more disk */dev/sdd* to the array.

**Prerequisites**

-   Enough disks for conversion.
-   The mdadm package is installed.
-   Ensure the intended conversion is supported. See [Supported RAID
    conversions](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/managing-raid_managing-storage-devices#supported-raid-conversions_managing-raid).

**Procedure**

1.  Convert the RAID /dev/md0 to RAID level *5*:
```
# mdadm --grow --level=5 -n 3 /dev/md0 --force
```
2.  Add a new disk to the array:
```
# mdadm --manage /dev/md0 --add /dev/sdd
```

**Verification**

Verify if the RAID level is converted:
```
# mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Thu Oct 13 15:17:39 2022
        Raid Level : raid0
        Array Size : 18649600 (17.79 GiB 19.10 GB)
      Raid Devices : 5
[...]
```

**ADDITIONAL RESOURCES**

-   The ```mdadm(8)``` man page

## Converting a root disk to RAID1 after installation

This section describes how to convert a non-RAID root disk to a RAID1
mirror after installing Red Hat Enterprise Linux 8.

On the PowerPC (PPC) architecture, take the following additional steps:

**Prerequisites**

-   The instructions in the following Red Hat Knowledgebase article are
    completed: [How do I convert my root disk to RAID1 after
    installation of Red Hat Enterprise Linux
    7?](https://access.redhat.com/solutions/2390831).

**Procedure**

1.  Copy the contents of the PowerPC Reference Platform (PReP) boot
    partition from */dev/sda1* to */dev/sdb1*:

> \# dd if=*/dev/sda1* of=*/dev/sdb1*

2.  Update the prep and boot flag on the first partition on both disks:

$ parted */dev/sda* set 1 prep on
$ parted */dev/sda* set 1 boot on

$ parted */dev/sdb* set 1 prep on
$ parted */dev/sdb* set 1 boot on

**Note**

Executing the grub2-install */dev/sda* command does not work on a
PowerPC machine and returns an error, but the system boots as expected.

## Creating advanced RAID devices

In some cases, you might want to install the operating system on an
array that is created before the installation completes. Usually, this
means setting up the /boot or root file system arrays on a complex RAID
device. In such cases, you might need to use array options that are not
supported by the Anaconda installer. To work around this, perform the
following steps.

**Note**

The limited Rescue Mode of the installer does not include man pages.
Both the mdadm and md man pages contain useful information for creating
custom RAID arrays, and might be needed throughout the workaround.

**Procedure**

1.  Insert the install disk.

2.  During the initial boot up, select **Rescue Mode** instead
    of **Install** or **Upgrade**. When the system fully boots
    into Rescue mode, you can see the command line terminal.

3.  From this terminal, execute the following commands:

    i.  Create RAID partitions on the target hard drives by using
        the parted command.

    ii. Manually create raid arrays by using the mdadm command from
        those partitions using any and all settings and options
        available.

4.  Optional: After creating arrays, create file systems on the arrays
    as well.

5.  Reboot the computer and select **Install** or **Upgrade** to
    install. As the Anaconda installer searches the disks in the system,
    it finds the pre-existing RAID devices.

6.  When asked about how to use the disks in the system, select **Custom
    Layout** and click **Next**. In the device listing, the pre-existing
    MD RAID devices are listed.

7.  Select a RAID device and click **Edit**.

8.  Configure its mount point and optionally the type of file system it
    should use if you did not create one earlier, and then
    click **Done**. Anaconda installs to this pre-existing RAID device,
    preserving the custom options you selected when you created it in
    Rescue Mode.

## Setting up email notifications to monitor a RAID

You can set up email alerts to monitor RAID with the ```mdadm``` tool. Once
the ```MAILADDR``` variable is set to the required email address, the
monitoring system sends the alerts to the added email address.

**Prerequisites**
-   The ```mdadm``` package is installed.
-   The mail service is set up.

**Procedure**
1.  Create the ```/etc/mdadm.conf``` configuration file for monitoring array
    by scanning the RAID details:
```
# mdadm --detail --scan >> /etc/mdadm.conf
```

2.  Open the ```/etc/mdadm.conf``` configuration file with a text editor of
    your choice and add the ```MAILADDR``` variable with the mail address for
    the notification. For example, add new line:
```
MAILADDR example@example.com>
```
Here, *example@example.com* is an email address to which you want to receive the alerts from the array monitoring.

3.  Save changes in the ```/etc/mdadm.conf``` file and close it.

**ADDITIONAL RESOURCES**
-   The ```mdadm.conf(5)``` man page

## Replacing a failed disk in RAID

You can reconstruct the data from the failed disks using the remaining
disks. RAID level and the total number of disks determines the minimum
amount of remaining disks needed for a successful data reconstruction.

In this procedure, the */dev/md0* RAID contains four disks. 
The */dev/sdd* disk has failed and you need to replace it with the */dev/sdf* disk.

**Prerequisites**
-   A spare disk for replacement.
-   The ```mdadm``` package is installed.

**Procedure**
1.  Check the failed disk:
    i.  View the kernel logs:
```
# journalctl -k -f
```
ii. Search for a message similar to the following:
```
md/raid:md0: Disk failure on sdd, disabling device.

md/raid:md0: Operation continuing on 3 devices.
```

iii. Press **Ctrl**+**C** on your keyboard to exit the journalctl program.


2.  Mark the failed disk as faulty:
```
# mdadm --manage /dev/md0 --fail /dev/sdd
```

3.  Optional: Check if the failed disk was marked correctly:
```
# mdadm --detail /dev/md0
```

At the end of the output is a list of disks in the */dev/md0* RAID
where the disk */dev/sdd* has the **faulty** status:

```
Number   Major   Minor   RaidDevice State
   0       8       16        0      active sync   /dev/sdb
   1       8       32        1      active sync   /dev/sdc
   -       0        0        2      removed
   3       8       64        3      active sync   /dev/sde

   2       8       48        -      faulty   /dev/sdd
```

4.  Remove the failed disk from the RAID:

```
# mdadm --manage /dev/md0 --remove /dev/sdd
```

**Warning**

 If your RAID cannot withstand another disk failure, do not remove any
 disk until the new disk has the **active sync** status. You can
 monitor the progress using the watch cat /proc/mdstat command.

5.  Add the new disk to the RAID:
```
# mdadm --manage /dev/md0 --add /dev/sdf
```

 The */dev/md0* RAID now includes the new disk */dev/sdf* and
 the mdadm service will automatically starts copying data to it from
 other disks.

**Verification**

-   Check the details of the array:

```
# mdadm --detail /dev/md0
```

 If this command shows a list of disks in the */dev/md0* RAID where the
 new disk has **spare rebuilding** status at the end of the output,
 data is still being copied to it from other disks:
```
Number   Major   Minor   RaidDevice State
   0       8       16        0      active sync   /dev/sdb
   1       8       32        1      active sync   /dev/sdc
   4       8       80        2      spare rebuilding   /dev/sdf
   3       8       64        3      active sync   /dev/sde
```

After data copying is finished, the new disk has an **active sync** status.

**ADDITIONAL RESOURCES**

-   [Setting up email notifications to monitor a
    RAID](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/managing-raid_managing-storage-devices#setting-up-email-notifications-to-monitor-a-raid_managing-raid)

## Repairing RAID disks

This procedure describes how to repair disks in a RAID array.

**Prerequisites**
-   The ```mdadm``` package is installed.

**Procedure**
1.  Check the array for the failed disks behavior:
```
# echo check > /sys/block/md0/md/sync_action
```
This checks the array and the ```/sys/block/md0/md/sync_action``` file shows the sync action.

2.  Open the ```/sys/block/md0/md/sync_action``` file with the text editor of
    your choice and see if there is any message about disk
    synchronization failures.

3.  View the ```/sys/block/md0/md/mismatch_cnt``` file. If
    the ```mismatch_cnt``` parameter is not ```0```, it means that the RAID disks
    need repair.

4.  Repair the disks in the array:
```
# echo repair > /sys/block/md0/md/sync_action
```

This repairs the disks in the array and writes the result into the ```/sys/block/md0/md/sync_action``` file.

5.  View the synchronization progress:
```
 \# cat /sys/block/*md0*/md/sync_action
 repair

 \# cat /proc/mdstat
 Personalities : \[raid0\] \[raid6\] \[raid5\] \[raid4\] \[raid1\]
 md0 : active raid1 sdg\[1\] dm-3\[0\]
 	511040 blocks super 1.2 \[2/2\] \[UU\]
 unused devices: \<none\>
```

Source [Link](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_storage_devices/managing-raid_managing-storage-devices#raid-types_managing-raid)







