# How to start Eewids

* [Requirements](#requirements)
  * [Minimal setup (running on local machine)](#minimal-setup-running-on-local-machine)
  * [Getting/Building Kismet Remote Capture](#gettingbuilding-kismet-remote-capture)
* [Start Eewids](#start-eewids)
  * [Starting the easy way (running on local machine)](#starting-the-easy-way-running-on-local-machine)
  * [Starting Kismet remote capture separately](#starting-kismet-remote-capture-separately)

## Requirements

### Minimal setup (running on local machine)

To run Eewids you need

* a [WiFi card](https://aircrack-ng.org/doku.php?id=compatible_cards) that is able to go into monitor mode and
* docker and docker-compose installed and set up on your machine.

### Getting/Building Kismet Remote Capture

*Note: The steps below are not needed for a simple test of Eewids and are only for distributed sources. You may skip and go directly to the ['start section'](#start-eewids).*

To really make use of Eewids you'll most likely want to have various sources of captured data. Therefore you need at least one machine that runs Eewids and multiple systems/routers or alike which have Kismet remote capture installed and report to Eewids afterwards.

For Arch Linux a PKGBUILD is available on the [AUR](https://aur.archlinux.org/packages/kismet-git/) which easily builds Kismet with Kismet remote capture.

If there is no Kismet-git package for your distribution, you have to follow the guidelines on [Kismet's GitHub page](https://github.com/kismetwireless/kismet/blob/master/README) to compile and install it. As long as there is no official release of Kismet's new code the process will be like this, sorry.

The commandy below may work as an entrypoint to only compile the remote capture tools (Kismet server itself is provided by Eewids). As Kismet development changes a lot, please have a look at Kismet's GitHub page.

```
sudo apt-get update && apt-get install git build-essential \
            pkg-config zlib1g-dev libnl-3-dev libnl-genl-3-dev libcap-dev \
            libpcap-dev libncurses5-dev libnm-dev libdw-dev \
            libsqlite3-dev libprotobuf-dev libprotobuf-c-dev \
            protobuf-compiler protobuf-c-compiler
git clone https://github.com/kismetwireless/kismet.git
cd kismet
./configure --enable-capture-tools-only --disable-python-tools
make
make suidinstall
```
Please go to the section below to see how to start Eewids with separate Kismet remote capture.

## Start Eewids

### Starting the easy way (running on local machine)

If you just want to give it a shot and you have a computer with a compatible WiFi card and docker and docker-compose installed (see [requirements](#requirements)), you may just use the start.sh in main directory of the repo: 

```
git clone https://github.com/techge/eewids.git
cd eewids
sudo ./start.sh wlan0
```
Where ```wlan0``` is your Wi-Fi interface.

Now visit http://localhost:3000 for grafana visualization and/or have a look at the services.

### Starting Kismet remote capture separately

Type in the following commands on the machine which should process the containers:

```
git clone https://github.com/techge/eewids.git
cd eewids
sudo ./start.sh --server
```

Now open a command line on the host which captures the traffic and type in the following:

```
kismet_cap_linux_wifi --connect docker-machine:3501 --source=wlan0
``` 
where `docker-machine` is the hostname of the machine you entered the start.sh script command.

