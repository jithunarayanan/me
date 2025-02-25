## Creating a partition table on a disk with parted
Use the parted utility to format a block device with a partition table more easily.

**Warning**

Formatting a block device with a partition table deletes all data stored on the device.

**Procedure**

Start the interactive parted shell:

`# parted *block-device*`

Determine if there already is a partition table on the device:

`# (parted) print`
If the device already contains partitions, they will be deleted in the following steps.

## Create the new partition table:

`# (parted) mklabel *table-type*`
Replace table-type with with the intended partition table type:

msdos for MBR
gpt for GPT

**Creating a GUID Partition Table (GPT) table**

To create a GPT table on the disk, use:

`# (parted) mklabel gpt`

The changes start applying after you enter this command.

View the partition table to confirm that it is created:

`# (parted) print`

Exit the parted shell:

`# (parted) quit`

**ADDITIONAL RESOURCES**
parted(8) man page.

## Viewing the partition table with parted
Display the partition table of a block device to see the partition layout and details about individual partitions. You can view the partition table on a block device using the parted utility.

**Procedure**

Start the parted utility. For example, the following output lists the device /dev/sda:

`# parted /dev/sda`
View the partition table:

`# (parted) print`
```
Model: ATA SAMSUNG MZNLN256 (scsi)
Disk /dev/sda: 256GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type      File system  Flags
 1      1049kB  269MB   268MB   primary   xfs          boot
 2      269MB   34.6GB  34.4GB  primary
 3      34.6GB  45.4GB  10.7GB  primary
 4      45.4GB  256GB   211GB   extended
 5      45.4GB  256GB   211GB   logical
```
Optional: Switch to the device you want to examine next:

`# (parted) select block-device`

For a detailed description of the print command output, see the following:
```
Model: ATA SAMSUNG MZNLN256 (scsi)
The disk type, manufacturer, model number, and interface.
Disk /dev/sda: 256GB
The file path to the block device and the storage capacity.
Partition Table: msdos
The disk label type.
Number
The partition number. For example, the partition with minor number 1 corresponds to /dev/sda1.
Start and End
The location on the device where the partition starts and ends.
Type
Valid types are metadata, free, primary, extended, or logical.
File system
The file system type. If the File system field of a device shows no value, this means that its file system type is unknown. The parted utility cannot recognize the file system on encrypted devices.
Flags
Lists the flags set for the partition. Available flags are boot, root, swap, hidden, raid, lvm, or lba.

**ADDITIONAL RESOURCES**
parted(8) man page.

## Creating a partition with parted
As a system administrator, you can create new partitions on a disk by using the parted utility.

> **Note:**
The required partitions are swap, /boot/, and / (root).

**Prerequisites**

A partition table on the disk.
If the partition you want to create is larger than 2TiB, format the disk with the GUID Partition Table (GPT).
Procedure

Start the parted utility:

`# parted block-device`
View the current partition table to determine if there is enough free space:

`# (parted) print`
Resize the partition in case there is not enough free space.
From the partition table, determine:

The start and end points of the new partition.
On MBR, what partition type it should be.
Create the new partition:

`# (parted) mkpart *part-type name fs-type start end*`

- Replace part-type with with primary, logical, or extended. This applies only to the MBR partition table.
- Replace name with an arbitrary partition name. This is required for GPT partition tables.
- Replace fs-type with xfs, ext2, ext3, ext4, fat16, fat32, hfs, hfs+, linux-swap, ntfs, or reiserfs. The fs-type parameter is optional. Note that the parted utility does not create the file system on the partition.
- Replace start and end with the sizes that determine the starting and ending points of the partition, counting from the beginning of the disk. You can use size suffixes, such as 512MiB, 20GiB, or 1.5TiB. The default size is in megabytes.

## Creating a small primary partition

To create a primary partition from 1024MiB until 2048MiB on an MBR table, use:

`# (parted) mkpart primary 1024MiB 2048MiB`
The changes start applying after you enter the command.

View the partition table to confirm that the created partition is in the partition table with the correct partition type, file system type, and size:

`# (parted) print`
Exit the parted shell:

`# (parted) quit`
Register the new device node:

`# udevadm settle`
Verify that the kernel recognizes the new partition:

`# cat /proc/partitions`

**ADDITIONAL RESOURCES**
parted(8) man page.

Creating a partition table on a disk with parted.
Resizing a partition with parted

# Setting a partition type with fdisk
You can set a partition type or flag, using the fdisk utility.

**Prerequisites**

A partition on the disk.

**Procedure**

Start the interactive fdisk shell:

`# fdisk block-device`
View the current partition table to determine the minor partition number:

Command (m for help): print
You can see the current partition type in the Type column and its corresponding type ID in the Id column.

Enter the partition type command and select a partition using its minor number:

Command (m for help): type
Partition number (1,2,3 default 3): 2
Optional: View the list in hexadecimal codes:

Hex code (type L to list all codes): L
Set the partition type:

Hex code (type L to list all codes): 8e
Write your changes and exit the fdisk shell:

Command (m for help): write
The partition table has been altered.
Syncing disks.
Verify your changes:

`# fdisk --list block-device`
4.5. Resizing a partition with parted
Using the parted utility, extend a partition to use unused disk space, or shrink a partition to use its capacity for different purposes.

**Prerequisites**

Back up the data before shrinking a partition.
If the partition you want to create is larger than 2TiB, format the disk with the GUID Partition Table (GPT).
If you want to shrink the partition, first shrink the file system so that it is not larger than the resized partition.
Note
XFS does not support shrinking.

Procedure

Start the parted utility:

`# parted block-device`
View the current partition table:

`# (parted) print`
From the partition table, determine:

The minor number of the partition.
The location of the existing partition and its new ending point after resizing.
Resize the partition:

`# (parted) resizepart 1 2GiB`
Replace 1 with the minor number of the partition that you are resizing.
Replace 2 with the size that determines the new ending point of the resized partition, counting from the beginning of the disk. You can use size suffixes, such as 512MiB, 20GiB, or 1.5TiB. The default size is in megabytes.
View the partition table to confirm that the resized partition is in the partition table with the correct size:

`# (parted) print`
Exit the parted shell:

`# (parted) quit`
Verify that the kernel registers the new partition:

`# cat /proc/partitions`
Optional: If you extended the partition, extend the file system on it as well.

**ADDITIONAL RESOURCES**
parted(8) man page.

Creating a partition table on a disk with parted
Resizing an ext3 file system
Resizing an ext4 file system
Increasing the size of an XFS file system
4.6. Removing a partition with parted
Using the parted utility, you can remove a disk partition to free up disk space.

**Warning**
Removing a partition deletes all data stored on the partition.

**Procedure**
Start the interactive parted shell:

`# parted block-device`
Replace block-device with the path to the device where you want to remove a partition: for example, /dev/sda.
View the current partition table to determine the minor number of the partition to remove:

`(parted) print`
Remove the partition:

`(parted) rm *minor-number*`
Replace minor-number with the minor number of the partition you want to remove.
The changes start applying as soon as you enter this command.

Verify that you have removed the partition from the partition table:

`(parted) print`
Exit the parted shell:

`(parted) quit`
Verify that the kernel registers that the partition is removed:

`# cat /proc/partitions`
Remove the partition from the /etc/fstab file, if it is present. Find the line that declares the removed partition, and remove it from the file.
Regenerate mount units so that your system registers the new /etc/fstab configuration:

`# systemctl daemon-reload`
If you have deleted a swap partition or removed pieces of LVM, remove all references to the partition from the kernel command line:

List active kernel options and see if any option references the removed partition:

`# grubby --info=ALL`
Remove the kernel options that reference the removed partition:

`# grubby --update-kernel=ALL --remove-args="option"`
To register the changes in the early boot system, rebuild the initramfs file system:

`# dracut --force --verbose`

**ADDITIONAL RESOURCES**
parted(8) man page.
