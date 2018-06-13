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
    then echo "Please run as root or with 'sudo'."
    exit
fi

# See if docker daemon is runnning and start otherwise
if [ \! -e "/var/run/docker.sock" ]
then
    echo "systemctl start docker"
    systemctl start docker
fi

# Instead of running the container as a specific user
# (see http://docs.grafana.org/installation/docker/#grafana-container-
#  using-bind-mounts)
# we will just change the owner rights to standard user id
if [ ! -d "data/grafana" ]; then
    mkdir -p data/grafana
    echo "Creating folder data/grafana and change owner rights for grafana:"
    echo "chown 472:472 data/grafana"
    chown 472:472 data/grafana
fi

if [ "$1" == "--server" ]
then

    echo "docker-compose up -d ..."
    docker-compose up -d

    echo
    echo ######################################################################
    echo you could now connect your source to the kismet server via
    echo /usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlan0
    echo or alike ...
    echo
    echo Afterwards, connect to http://localhost:3000 and 
    echo login with admin:admin
    echo ######################################################################
    echo

    docker-compose logs --follow logprint

    echo "killing everything now :)"
    docker-compose down

else

    echo "docker-compose up ..."
    docker-compose -f docker-compose.yml \
                   -f docker-compose.standalone.yml up -d

    echo "connecting interface with kismet..."
    sleep 3
    # inspired by Kismet wireless...
    # https://github.com/kismetwireless/kismet/blob/master/packaging/docker/
    PHY=$(cat /sys/class/net/"$1"/phy80211/name)
    PID=$(docker container inspect -f '{{.State.Pid}}' eewids_kismet-server_1)
    echo "iw phy $PHY set netns $PID"
    iw phy "$PHY" set netns "$PID"

    docker-compose logs --follow logprint

    echo "killing everything now :)"
    docker-compose down

    echo "Try to restore WiFi (based on NetworkManager)"
    sleep 3
    nmcli device set $1 managed true

fi
