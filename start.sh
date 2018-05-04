#!/bin/sh

if [ \! -e "/var/run/docker.sock" ]
then
    echo "sudo systemctl start docker"
    sudo systemctl start docker
fi

echo "docker-compose up -d ..."
docker-compose up -d

sleep 3
echo "starting kismet remote capture ..."
/usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlan0 &

echo "attaching to example"
docker-compose logs --follow rogueAP

echo "killing everything :)"
docker-compose down
kill %%

echo "I am just waiting some time..."
sleep 3

echo "Try to restore WiFi"
nmcli device set wlan0 managed true
