# How to start Eewids

## Requirements

To run Eewids you need

* a [WiFi card](https://aircrack-ng.org/doku.php?id=compatible_cards) that is able to go into monitor mode and
* docker and docker-compose installed and set up on your machine.

## Start Eewids

### Starting the easy way (running on local machine)

If you just want to give it a shot and you have a computer with a compatible WiFi card and docker and docker-compose installed (see [requirements](#requirements)), you may just use the start.sh in main directory of the repo: 

```
git clone https://github.com/techge/eewids.git
cd eewids
sudo ./start.sh wlan0
```
Where ```wlan0``` is your Wi-Fi interface.

Now visit http://localhost:3000 for grafana visualization and/or get familiar with [the services](/plugins).

### Starting Eewids and connect capture sources manually 

To only start all server components of Eewids, type the following commands on the machine which should process the main parts of Eewids (=the server):

```
git clone https://github.com/techge/eewids.git
cd eewids
sudo ./start.sh --server
```

To use the capture tool separately e.g. to connect multiple sources to Eewids, you need to build the capture tool first on the machine. It needs libpcap and librabbitmq to get build successfully. For example on a Debian-based system you would need to install the following:

```
sudo apt-get update
sudo apt-get install \
    build-essential \
    libcap-dev \
    libnl-3-dev \
    libnl-genl-3-dev \
    libnm-dev \
    libpcap-dev \
    librabbitmq-dev \
    pkg-config
```

After installing the depencies you can clone the repo and build the capture tool.

```
git clone https://github.com/techge/eewids.git
cd eewids/kiscap2amqp
./configure
make
```

Now you can start the capture tool by typing the following:

```
./capture_linux_wifi/kiscap2amqp_linux_wifi --source wlan0 --rabbitmq localhost:5672 --capexchange capture-raw
``` 

where `wlan0` is the Wi-Fi interface and `--rabbitmq` points to the RabbitMQ server on machine you entered the `start.sh --server` script command.

