# Easily Expandable Wireless Intrusion Detection System
**Note:** This project is still in development and far away from being ready or perfect. However, feel free to play around and open issues if you see something interesting. Also have a look at the [getting-started](doc/getting-started.md) section.

* [Background](#background)
  * [Existing WIDS Tools](#existing-wids-tools)
  * [Why Not Just Expanding Existing Programs?](#why-not-just-expanding-existing-programs)
* [Main Idea of EEWIDS](#main-idea-of-eewids)
  * [Basis Kismet](#basis-kismet)
  * [Message Broker RabbitMQ](#message-broker-rabbitmq)
  * [Analyzing and Visualisation](#analyzing-and-visualisation)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

## Background 
### Existing WIDS Tools
[Analyzing 0x90/wifi-arsenal](https://github.com/techge/wifi-arsenal) especially in search of wireless intrusion detection systems (WIDS) I realized that there just is no complete ready-to-go solution yet, at least regarding free and open source software (FOSS). For me a WIDS should serve the following needs:

* detection of most of the known Wi-Fi attacks
* scalability and thus being able to work within big organizations
* simple expandability (there are always more attacks to come ;-))

Although there is indeed software on GitHub which can be used to detect Wi-Fi attacks, they are usually specialized on some attacks and/or they are hobby projects which would not fit in setups of bigger environments. Please have a look at the defence-related Wi-Fi tools on the [wifi-arsenal](https://github.com/techge/wifi-arsenal#defencedetection) list.

An exception should be mentioned: [Kismet](https://www.kismetwireless.net/). It is probably the most famous and complete FOSS Wi-Fi solution and very popular. Still, it does not seem to fulfill the above necessities completely. And it is probably not the objective of Kismet to be a full-features WIDS either. Instead it has many features for pentesting Wi-Fi networks and other interesting stuff.

### Why Not Just Expanding Existing Programs?
One solution would be to simply add needed functionality to Kismet. And this is definitely a good idea and I encourage everyone to improve the code of Kismet. Some needs mentioned above could be solved with a microservice approach more generally though. This is exactly what EEWIDS tries to achieve. By creating a containerized framework EEWDIS enables

* scalability
* working easily in setups of bigger organizations 
* the possibility to add functionality easily (see [below](#analyzing-and-visualization))

## Main Idea of EEWIDS
![Simple layout sketch of EEWIDS](framework_layout.png?raw=true)

### Basis Kismet
EEWIDS uses Kismet as a basis. Thus, it uses Kismet's advantages and tries to add functionality by using container techniques. As Kismet is under heavy development right now, EEWIDS uses the [git version of Kismet](https://github.com/kismetwireless/kismet), which is completely different to the last release from 2016. The Kismet remote capture (which replaces the former Kismet drone) is the only piece of software, which can not be containerized. The Kismet remote captures have to run on the machine which contains a Wi-Fi card which is able to monitor the traffic. As Kismet is very popular the Kismet remote capture will run on many different machines and platforms, e.g. OpenWrt. Therefore, it is better to use Kismet as a basis for capturing the data instead of building an own system.

The Kismet remote capture will send the data to a Kismet server instance which is running in a container. By using the Kismet server we will be informed about every attack which Kismet did detect and thus we can reuse the work already done on this side. EEWIDS will attach to the Kismet server to:

* pulling the pcap-ng data stream which contains all data captured
* pulling all alerts raised by Kismet server itself

### Message Broker RabbitMQ
Both kind of information will be parsed and submitted to a Message Broker afterwards. The Message Broker is the central point of EEWIDS. By using RabbitMQ -- one of the most popular systems of its kind -- it is easily possible to subscribe to a needed information. This is supposed to be the big advantage for developers. Thus, instead of capturing and parsing Wi-Fi packets itself, a detection method only needs to subscribe to the needed information and will receive it directly from the Message Broker. Furthermore, the developer can use any programming language or system which is needed for this kind of detection, without bothering C++ or other stuff, which may would be necessary for Kismet plugins.

### Analyzing and Visualization
The actual analyzing is done in services dedicated to this task. Instead of parsing package, looking for Beacons and analyzing it afterwards, a service will just subscribe to all Beacon frames. All other frames are not of interest. The service does not need to parse the Beacon frames, it just needs to access the json-formatted information it got from the Message Broker, e.g. data['wlan.SSID'] or data['wlan.BSSID']. This can be done independent of the programming language, as most of them speaks json and are able to access RabbitMQ. This should be indeed possible for every language which already has a client listed on [RabbitMQ website](https://www.rabbitmq.com/devtools.html).

Another advantage is the freedom of choice of visualization/analyzing software. It is easily possible to include either influxdata's TICK stack or the elastic stack, both Open Source analyzing software which also have anomaly detection methods. These stacks and other software already have interfaces to access RabbitMQ and to read json-formatted data and thus it is easy to extract the collected information as needed.

This should make is easy to extend EEWIDS in various ways. Let's see what can happen.
