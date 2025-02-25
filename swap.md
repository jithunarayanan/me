# Linux swap
Swap space in Linux is used when the amount of physical memory (RAM) is full. If the system needs more memory resources and the RAM is full, 
inactive pages in memory are moved to the swap space. While swap space can help machines with a small amount of RAM, it should not be considered 
a replacement for more RAM. Swap space is located on hard drives, which have a slower access time than physical memory. Swap space can be a 
dedicated swap partition (recommended), a swap file, or a combination of swap partitions and swap files. Note that Btrfs does not support swap space.

Sometimes it is necessary to add more swap space after installation. For example, you may upgrade the amount of RAM in your system from 1 GB to 2 GB, 
but there is only 2 GB of swap space. It might be advantageous to increase the amount of swap space to 4 GB if you perform memory-intense operations or 
run applications that require a large amount of memory.

You have three options: create a new swap partition, create a new swap file, or extend swap on an existing LVM2 logical volume. It is recommended that 
you extend an existing logical volume.


**Recommended System Swap Space**
-------------------------------------------------------------------------------------------------------------------------------------
**Amount of RAM in the system**	    **Recommended swap space**	                   **Recommended swap space if allowing for hibernation**
-------------------------------------------------------------------------------------------------------------------------------------
⩽ 2GB                               2 times the amount of RAM                      3 times the amount of RAM
> 2GB                               – 8 GB	Equal to the amount of RAM             2 times the amount of RAM
> 8GB                               – 64 GB	At least 4 GB	                         1.5 times the amount of RAM
> 64GB                              At least 4 GB	                                 Hibernation not recommended
-------------------------------------------------------------------------------------------------------------------------------------

## Extending Swap on an LVM2 Logical Volume
By default, Red Hat Enterprise Linux 7 uses all available space during installation. If this is the case with your system, 
then you must first add a new physical volume to the volume group used by the swap space.
After adding additional storage to the swap space's volume group, it is now possible to extend it. To do so, perform the following 
procedure (assuming /dev/VolGroup00/LogVol01 is the volume you want to extend by 2 GB):
This Procedure Extending Swap on an LVM2 Logical Volume

Disable swapping for the associated logical volume:
```
# swapoff -v /dev/VolGroup00/LogVol01
```
Resize the LVM2 logical volume by 2 GB:
```
# lvresize /dev/VolGroup00/LogVol01 -L +2G
```
Format the new swap space:
```
# mkswap /dev/VolGroup00/LogVol01
```
Enable the extended logical volume:
```
# swapon -v /dev/VolGroup00/LogVol01
```
To test if the swap logical volume was successfully extended and activated, inspect active swap space:
```
$ cat /proc/swaps
$ free -h
```

## Creating an LVM2 Logical Volume for Swap
To add a swap volume group 2 GB in size, assuming /dev/VolGroup00/LogVol02 is the swap volume you want to add:

Create the LVM2 logical volume of size 2 GB:
```
# lvcreate VolGroup00 -n LogVol02 -L 2G
```
Format the new swap space:
```
# mkswap /dev/VolGroup00/LogVol02
```

Add the following entry to the /etc/fstab file:
```
/dev/VolGroup00/LogVol02   swap     swap    defaults     0 0
```

Regenerate mount units so that your system registers the new configuration:
```
# systemctl daemon-reload
```

Activate swap on the logical volume:
```
# swapon -v /dev/VolGroup00/LogVol02
```

To test if the swap logical volume was successfully created and activated, inspect active swap space:
```
$ cat /proc/swaps
$ free -h
```

## Creating a Swap File
To add a swap file:
Procedure 15.2. Add a Swap File

Determine the size of the new swap file in megabytes and multiply by 1024 to determine the number of blocks. For example, the block size of a 64 MB swap file is 65536.
Create an empty file:
```
# dd if=/dev/zero of=/swapfile bs=1024 count=65536
```

Replace count with the value equal to the desired block size.
Set up the swap file with the command:
```
# mkswap /swapfile
```

Change the security of the swap file so it is not world readable.
```
# chmod 0600 /swapfile
```

To enable the swap file at boot time, edit /etc/fstab as root to include the following entry:
```
/swapfile          swap            swap    defaults        0 0
```

The next time the system boots, it activates the new swap file.
Regenerate mount units so that your system registers the new /etc/fstab configuration:
```
# systemctl daemon-reload
```

To activate the swap file immediately:
```
# swapon /swapfile
```

To test if the new swap file was successfully created and activated, inspect active swap space:
```
$ cat /proc/swaps
$ free -h
```
