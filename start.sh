#!/bin/sh

if [ $# -lt 1 ]; then
    echo
    echo "Usage: sudo ./start.sh [wifi-interface | --server]"
    echo
    echo "e.g. sudo ./start.sh wlan0    # for standalone version"
    echo "or   sudo ./start.sh --server # only start server without capturing"
    echo
    exit
fi

if [ "$EUID" -ne 0 ]
    then echo "Please run as root."
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

docker-compose up -d

if [ "$1" == "--server" ]
then

    echo
    echo "######################################################################"
    echo you could now connect your source to the kismet server via
    echo /usr/bin/kismet_cap_linux_wifi --connect localhost:3501 --source=wlan0
    echo or alike ...
    echo
    echo Afterwards, connect to http://localhost:3000 and 
    echo login with admin:admin
    echo "######################################################################"
    echo
    echo Press Ctrl-c to end Eewids
    echo
    docker-compose logs --follow logprint

    echo "killing everything now :)"
    echo
    docker-compose down

else

    export WIFI_DEVICE=$1
    docker-compose -f docker-compose.yml \
                   -f docker-compose.standalone.yml run -d kismet-remote 

    echo
    echo "######################################################################"
    echo
    echo Connect to http://localhost:3000 and 
    echo login with admin:admin
    echo
    echo Press Enter to end Eewids
    echo
    echo "######################################################################"

    read

    echo "Killing everything now :)"
    echo
    docker-compose -f docker-compose.yml \
                   -f docker-compose.standalone.yml down

    echo "Try to restore WiFi (based on NetworkManager)"
    sleep 3
    nmcli device set $1 managed true

fi
