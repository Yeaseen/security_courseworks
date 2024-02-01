# Problems regarding running SEEDUbuntu-16.04-32bit.vmdk
## Problem 1:
```bash
Kernel driver not installed (rc=-1908)

The VirtualBox Linux kernel driver (vboxdrv) is either not loaded or there is a permission problem with /dev/vboxdrv. Please install virtualbox-dkms package and load the kernel module by executing

modprobe vboxdrv
as root. If it is available in your distribution, you should install the DKMS package first. This package keeps track of Linux kernel changes and recompiles the vboxdrv kernel module if necessary.

where: suplibOsInit what: 3 VERR_VM_DRIVER_NOT_INSTALLED (-1908) - The support driver is not installed. On linux, open returned ENOENT.
```
## Solution to Problem 1: 
I ran the following commands to install the necessary driver.

```bash
sudo apt update
sudo apt install --reinstall linux-headers-$(uname -r) virtualbox-dkms dkms
sudo modprobe vboxdrv
```
## Problem 2:
```bash
Result Code: NS_RROR_FAILURE (0x80004005)
VirtualBox - Guru Meditation

A critical error has occurred while running the virtual machine and machine
execution has been stopped.
```
So, I read the VirtualBox log file and found the error: "This kernel requires the following features not present on the CPU: pae"
If Enable PAE/NX is not checked, you won't be able to boot the kernel.

## Solution to Problem 2:
```bash
1- Open VM VirtualBox

2- file -> Settings -> System -> Processor

3- Check Extended Features : Enable PAE/NX
```

