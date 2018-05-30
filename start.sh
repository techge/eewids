#!/bin/sh

# TODO check if docker must be run with root privs

# TODO add option for using remote capture with docker container

if [ $# -lt 1 ]; then
    echo "Usage: ./start.sh [wifi-interface]"
    echo
    echo "e.g. ./start.sh wlan0"
    echo
    exit
fi

if [ \! -e "/var/run/docker.sock" ]
then
    echo "sudo systemctl start docker"
    sudo systemctl start docker
fi

echo "docker-compose up -d ..."
docker-compose up -d

echo "starting kismet remote capture ..."
sleep 3
/usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=$1 &

docker-compose logs --follow logprint

echo "killing everything now :)"
docker-compose down

kill %%

echo "Try to restore WiFi"
sleep 3
nmcli device set $1 managed true
