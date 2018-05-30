#!/bin/sh

# simple deploy script for BOWL test setup
# usage: deploy.sh <IP of Kismet server>

wget -nc https://github.com/techge/eewids/raw/master/kismet-remote/kismet-remote_2018git-1_i386_pentium.ipk --no-check-certificate
wget -nc https://github.com/techge/eewids/raw/master/kismet-remote/libprotobuf-c_v1.2.1_i386_pentium.ipk --no-check-certificate
opkg install kismet-remote_2018git-1_i386_pentium.ipk libprotobuf-c_v1.2.1_i386_pentium.ipk
ssh -f wifi@$1 -L 3501:$1:3501 -N
kismet_cap_linux_wifi --connect localhost:3501 --source wlan0
