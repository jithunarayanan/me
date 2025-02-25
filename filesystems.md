# Creating an XFS file system with mkfs.xfs
This procedure describes how to create an XFS file system on a block device.


## XFS Filesystem

**Procedure**

To create the file system:

If the device is a regular partition, an LVM volume, an MD volume, a disk, or a similar device, use the following command:

```
# mkfs.xfs *block-device*
```
Replace block-device with the path to the block device. For example, `/dev/sdb1`, `/dev/disk/by-uuid/05e99ec8-def1-4a5e-8a9d-5945339ceb2a`, 
or `/dev/my-volgroup/my-lv`.

In general, the default options are optimal for common use.
When using `mkfs.xfs` on a block device containing an existing file system, add the `-f` option to overwrite that file system.

To create the file system on a hardware RAID device, check if the system correctly detects the stripe geometry of the device:

If the stripe geometry information is correct, no additional options are needed. Create the file system:
```
# mkfs.xfs block-device
```
If the information is incorrect, specify stripe geometry manually with the su and sw parameters of the -d option. The su parameter specifies the RAID chunk size, and the sw parameter specifies the number of data disks in the RAID device.

For example:
```
# mkfs.xfs -d su=64k,sw=4 /dev/sda3
```
Use the following command to wait for the system to register the new device node:
```
# udevadm settle
```
ADDITIONAL RESOURCES
```
mkfs.xfs(8) man page.
```


### Increasing the size of an XFS file system with xfs_growfs
This procedure describes how to grow an XFS file system using the `xfs_growfs` utility.

**Prerequisites**

- Ensure that the underlying block device is of an appropriate size to hold the resized file system later. Use the 
appropriate resizing methods for the affected block device.

- Mount the XFS file system.

**Procedure**

- While the XFS file system is mounted, use the `xfs_growfs` utility to increase its size:

```
# xfs_growfs file-system -D new-size
```

- Replace `file-system` with the mount point of the XFS file system.
- With the `-D` option, replace new-size with the desired new size of the file system specified in the number of file system blocks.

	To find out the block size in kB of a given XFS file system, use the `xfs_info` utility:

```
# xfs_info block-device

...
data     =              bsize=4096
...
```
- Without the -D option, xfs_growfs grows the file system to the maximum size supported by the underlying device.


ADDITIONAL RESOURCES
```
xfs_growfs(8) man page.
```

# Creating an ext3/ext4 file system
As a system administrator, you can create an ext3 file system on a block device using `mkfs.ext3`/`mkfs.ext4` command.

**Prerequisites**
- A partition on your disk. For information about creating MBR or GPT partitions, see Creating a partition table on a disk with parted.

**Procedure**

To create an ext3 file system:

For a regular-partition device, an LVM volume, an MD volume, or a similar device, use the following command:
```
# mkfs.ext3 /dev/block_device
```
Replace `/dev/block_device` with the path to a block device.

For example, `/dev/sdb1`, `/dev/disk/by-uuid/05e99ec8-def1-4a5e-8a9d-5945339ceb2a`, or `/dev/my-volgroup/my-lv`. 
In general, the default options are optimal for most usage scenarios.

For striped block devices (for example, RAID5 arrays), the stripe geometry can be specified at the time of file 
system creation. Using proper stripe geometry enhances the performance of an ext3 file system. For example, 
to create a file system with a 64k stride (that is, 16 x 4096) on a 4k-block file system, use the following command:
```
# mkfs.ext3 -E stride=16,stripe-width=64 /dev/block_device
```
In the given example:

- stride=value: Specifies the RAID chunk size
- stripe-width=value: Specifies the number of data disks in a RAID device, or the number of stripe units in the stripe.

>**Note:**
To specify a UUID when creating a file system:
```
# mkfs.ext3 -U UUID /dev/block_device
# mkfs.ext4 -U UUID /dev/block_device
```
Replace UUID with the UUID you want to set: for example, `7cd65de3-e0be-41d9-b66d-96d749c02da7`.

Replace `/dev/block_device` with the path to an ext3/ext4 file system to have the UUID added to it: for example, `/dev/sda8`.

To specify a label when creating a file system:
```
# mkfs.ext3 -L label-name /dev/block_device
```
To view the created ext3/ext4 file system:
```
# blkid
```
ADDITIONAL RESOURCES
```
ext3/ext4 man page.
mkfs.ext3/mkfs.ext4 man page.
```

### Resizing an ext3/ext4 file system
As a system administrator, you can resize an ext3/ext4 file systems using the `resize2fs` utility. The `resize2fs` 
utility reads the size in units of file system block size, unless a suffix indicating a specific unit is used. 
The following suffixes indicate specific units:

- s (sectors) - `512` byte sectors
- K (kilobytes) - `1,024` bytes
- M (megabytes) - `1,048,576` bytes
- G (gigabytes) - `1,073,741,824` bytes
- T (terabytes) - `1,099,511,627,776` bytes

**Prerequisites**

- An ext3/ext4 file system.
- An underlying block device of an appropriate size to hold the file system after resizing.

**Procedure**

To resize an ext3/ext4 file system, take the following steps:

- To shrink and grow the size of an unmounted ext3 file system:
```
# umount /dev/block_device
# e2fsck -f /dev/block_device
# resize2fs /dev/block_device size
```
Replace */dev/block_device* with the path to the block device, for example ```/dev/sdb1```.

Replace size with the required resize value using `s`,` K`, `M`, `G,` and` T` suffixes.

An ext3/ext4 file system may be grown while mounted using the `resize2fs` command:
```
# resize2fs /mount/device size
```
>**Note:**
The size parameter is optional (and often redundant) when expanding. The `resize2fs` automatically expands to fill 
the available space of the container, usually a logical volume or partition.

To view the resized file system:
```
# df -h
```
