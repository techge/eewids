#!/bin/sh

if [ $# -lt 1 ]; then
    echo
    echo "Usage: sudo ./start.sh [wifi-interface | --server]"
    echo
    echo "e.g. sudo ./start.sh wlan0        # for standalone version"
    echo "or   sudo ./start.sh --server     # only start Kismet server"
    echo
    exit
fi

if [ "$EUID" -ne 0 ]
    then echo "Please run as root or with 'sudo'"
    exit
fi

if [ \! -e "/var/run/docker.sock" ]
then
    echo "systemctl start docker"
    systemctl start docker
fi

if [ "$1" == "--server" ]
then

    echo "docker-compose up -d ..."
    docker-compose up -d

    docker-compose logs --follow logprint
    # you could now connect to the kismet server via
    # /usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlan0

    echo "killing everything now :)"
    docker-compose down

else

    echo "docker-compose up ..."
    docker-compose -f docker-compose.yml \
                   -f docker-compose.standalone.yml up -d

    echo "connecting interface with kismet..."
    sleep 3
    # inspired by Kismet wireless...
    # https://github.com/kismetwireless/kismet/blob/master/packaging/docker/assign_wifi_to_docker.sh
    PHY=$(cat /sys/class/net/"$1"/phy80211/name)
    PID=$(docker container inspect -f '{{.State.Pid}}' eewids_kismet-server_1)
    iw phy "$PHY" set netns "$PID"

    docker-compose logs --follow logprint

    echo "killing everything now :)"
    docker-compose down

    echo "Try to restore WiFi (based on NetworkManager)"
    sleep 3
    nmcli device set $1 managed true

fi
