#!/bin/bash
DEV_SDA=$(sudo smartctl -a /dev/sda | grep -e M.2 -e 'Solid State Device')
DEV_SDB=$(sudo smartctl -a /dev/sdb | grep -e M.2 -e 'Solid State Device')
DEV_SDC=$(sudo smartctl -a /dev/sdc | grep -e M.2 -e 'Solid State Device')
NVME_DRIVE="/dev/sda"
if [[ $DEV_SDB == *"M.2"* || $DEV_SDB == *"Solid State Device"* ]]; then {
NVME_DRIVE="/dev/sdb"
} 
elif [[ $DEV_SDA == *"M.2"* || $DEV_SDA == *"Solid State Device"* ]]; then {
NVME_DRIVE="/dev/sda"
} 
elif [[ $DEV_SDC == *"M.2"* || $DEV_SDC == *"Solid State Device"* ]]; then {
NVME_DRIVE="/dev/sdc"
} 
fi

CHROOT_PATH="/nvmeroot"

INITBIN=/lib/systemd/systemd
EXT4_OPT="-o defaults -o errors=remount-ro -o discard"

modprobe ext4
#modprobe fuse

mkdir -p ${CHROOT_PATH}
mount -t ext4 ${EXT4_OPT} ${NVME_DRIVE} ${CHROOT_PATH}

cd ${CHROOT_PATH}
/bin/systemctl --no-block switch-root ${CHROOT_PATH}
