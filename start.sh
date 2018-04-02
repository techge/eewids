#!/bin/sh

if [ \! -f /var/run/docker.sock]
then
    echo "sudo systemctl start docker"
    sudo systemctl start docker
fi

echo "Starting RabbitMQ"
docker run -tid --net=host rabbitmq

echo "Starting Kismet Stuff"
docker run -tid --net=host eewids/kismet
sleep 5
/usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlp2s0 &

echo "Starting Rabbit-recv"
docker run -ti --net=host rabbit-recv

echo "killing everything :)"
docker stop $(docker ps -q)
kill %%

echo "I am just waiting some time..."
sleep 5

echo "Try to restore WiFi"
nmcli device set wlp2s0 managed true
