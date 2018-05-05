# How to start Eewids

## Requirements

* A machine on which you can execute a Kismet remote capture binary and that has a WiFi interface that is able to go into monitor mode. <!--TODO further explanation and notes are needed!-->
* A machine that can run Docker containers and docker-compose

### Kismet Remote Capture

For Arch Linux a PKGBUILD is available on the [AUR](https://aur.archlinux.org/packages/kismet-git/).

If there is no Kismet-git package for your distribution, you have to follow the guidelines on [Kismet's GitHub page](https://github.com/kismetwireless/kismet/blob/master/README) to compile and install it. As long as there is no official release of Kismet's new code the process will be like this, sorry.

## Start Eewids

Type in the following commands on the machine which should process the containers:

```
git clone https://github.com/techge/eewids.git
cd eewids
docker-compose up
```

Now open a command line on the host which captures the traffic and type in the following:

```
kismet_cap_linux_wifi --connect docker-machine:3501 --source=wlan0 &
``` 
where `docker-machine` is the hostname of the machine you entered the `docker-compose up` command.

### Starting the easy way - testing on local machine

If you just want to give it a shoot and you have a computer with a compatible WiFi card and Kismet-git installed, you may just use the start.sh in main directory of the repo. Please be aware, that you may have to adapt the Wi-Fi interface information or other parts in the script.
