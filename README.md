# Easily Expandable Wireless Intrusion Detection System

**Note:** While this project may is in a state in which it can be used, it still needs a lot of development and thus is far away from being ready or perfect. However, feel free to play around and open issues if you see something interesting. Also have a look at the [getting-started](doc/getting-started.md) section before starting.

## Background 
[Analyzing 0x90/wifi-arsenal](https://github.com/techge/wifi-arsenal) especially in search of wireless intrusion detection systems (WIDS) I realized that there just is no complete ready-to-go solution yet, at least regarding free and open source software (FOSS). For me a WIDS should

* detect most of the known Wi-Fi attacks,
* scale easily and thus be able to work within big organizations and
* be easily expandable.

Although there is indeed software on GitHub which can be used to detect Wi-Fi attacks, they are usually specialized on some attacks and/or they are hobby projects which would not fit in setups of bigger environments. Please have a look at the defence-related Wi-Fi tools on the [wifi-arsenal](https://github.com/techge/wifi-arsenal#defencedetection) list.

An exception should be mentioned: [Kismet](https://www.kismetwireless.net/). It is probably the most famous and complete FOSS Wi-Fi solution and very popular. Still, it does not seem to fulfill the above necessities. And it is probably not the objective of Kismet to be a full-featured WIDS either. Instead it has also many options for pentesting Wi-Fi networks and other interesting stuff.

## Main Idea of Eewids
![Simple layout sketch of Eewids](framework_layout.png?raw=true)

Eewids uses standard software for distributing and analyzing data. The data captured by Eewids' capture tool is sent directly to a message broker. Actually, the Message Broker is the central point of Eewids. By using RabbitMQ -- one of the most popular systems of its kind -- it is easily possible to subscribe to a needed information on many different environments. This is supposed to be the big advantage for developers. 

Let's look at a [honey pot](https://en.wikipedia.org/wiki/Honeypot_(computing)) detection as an example. Instead of parsing packages and looking for e.g. Beacon frames and analyzing it afterwards, the detection method will just subscribe for all Beacon frames arriving at the Message Broker. It doesn't have to care about the capture process at all. The other frames are not of interest for this method anyway. The created service does not need to parse the Beacon frames, it just needs to access the json-formatted information it got from the Message Broker, e.g. data['wlan.SSID'] or data['wlan.BSSID']. This can be done independently of the programming language, as most of them are already able to interpret json and to access RabbitMQ. This should be indeed possible for every language which already has a client listed on [RabbitMQ's website](https://www.rabbitmq.com/devtools.html).

Another advantage is the freedom of choice of visualization/analyzing software. It is easily possible to include either influxdata's [TICK stack](https://www.influxdata.com/time-series-platform/) or the [ElasticSearch stack](https://www.elastic.co/), both Open Source analyzing software which also have anomaly detection methods. These stacks and other software already have interfaces to access RabbitMQ and to read json-formatted data and thus it is easy to extract the collected information as needed. Eewids already integrates InfluxDB with Grafana for visualization of captured data.

This should make it easy to extend Eewids in various ways. Let's see what can happen.

## TODOs

These are limitations and problems that would be nice to get addressed (beside a lot of others ;-) ):

* fix time problems -> in influxdb the time when telegraf is sending the data is stored -> we want to store the actual capture time. This might be decided by pcap on device or by RabbitMQ arrival time or something else
* pcapng-export tool -> export pcapng stream by getting all messages of the capture-raw exchange during a specific time frame and craft it to a pcapng
* look for the tag_keys problem: telegraf is getting the data as json from rabbitmq and is sending this data to influxdb - we can only use these values in the 'where' part of a query in grafana that we have defined as 'tag_keys' in etc/telegraf.conf before hand. this is most annoying
* Look if Kapacitor (Influx stack) could add any value to Eewids
* Add RabbitMQ metric to Grafana https://www.rabbitmq.com/prometheus.html
