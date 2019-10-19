#!/bin/bash

cd      "$(dirname "$0")"

sudo    apt-get update
sudo    apt-get install -y  wget gnupg debootstrap software-properties-common

sudo    rm      -rf rootfs* trusted.gpg*
sudo    mkdir   -p  rootfs

wget    'http://raspbian.raspberrypi.org/raspbian.public.key'       -O  -   |   \
            sudo    apt-key --keyring   ./trusted.gpg           add     -

sudo    debootstrap --keyring   ./trusted.gpg   --force-check-gpg               \
                    --variant=minbase       --components=main,contrib,rpi       \
                    --include=dirmngr,apt-transport-https                       \
                    --exclude=gcc-4.9-base,gcc-5-base,gcc-6-base,gcc-7-base     \
                    --arch=armhf    buster  rootfs                              \
                    http://raspbian.raspberrypi.org/raspbian/

sudo    rm  -f  trusted.gpg*

wget    'http://archive.raspberrypi.org/debian/raspberrypi.gpg.key' -O  -   |   \
            sudo    apt-key --keyring   rootfs/etc/apt/trusted.gpg add  -

echo    "deb http://archive.raspberrypi.org/debian/ buster main"    > raspi.list
sudo    cp  -f  raspi.list  rootfs/etc/apt/sources.list.d
rm          -f  raspi.list
sudo    rm  -rf rootfs/var/lib/apt/lists/*  rootfs/var/cache/apt/*  rootfs/dev/*

( cd rootfs ; sudo tar cfJ ../rootfs.tar.xz * )

sudo    rm  -rf rootfs

