# Rogue Access Point Detection

```
usage: rogueap.py [-h] [--rabbit_host HOST] [--rabbit_port PORT]
                  [--alert | --train] [--info]

Rogue access point detection for Eewids. Store your whitelist.yml and/or
blacklist.yml in folder 'lists', if needed.

optional arguments:
  -h, --help          show this help message and exit
  --rabbit_host HOST  Host of RabbitMQ server
  --rabbit_port PORT  Port of RabbitMQ server
  --alert             Send alerts for access points not on whitelist (instead
                      of warnings). Note that blacklist members will always
                      provoke an alert. Thus, this option is for whitelist
                      enforcement and this option can not get combined with
                      --train.
  --train             Create/use knownAP.yml of already seen access points. If
                      this flag is used, only access points never seen before
                      provoke a warning.
  --info              Send info instead of warning. Blacklist members will
                      always provoke an alert though.
```

## Characteristics

* scalable (it does not make any difference, if one service sees all or just one frame, therefore multiple workers can get started based on load)
* shared storage needed to allow scalability, e.g. for saving/using a knownAP list
* needs network connection to: 
  * RabbitMQ

## General Approach

The service for rogue access point detection looks for new/forbidden ESSIDs or ESSID/BSSID combinations seen by the remote capture. Alerts, warnings or infos are published consequently.

This service is called rogue access point detection, although this might be misleading as rogue AP is often referred to a WiFi AP connected to a secure network (see the wikipedia [article](https://en.wikipedia.org/wiki/Rogue_access_point)). However this tool is maybe more about finding ["evil twins"](https://en.wikipedia.org/wiki/Evil_twin_(wireless_networks)) or [honeypots](https://en.wikipedia.org/wiki/Honeypot_(computing)) which are indeed "rogue" access points within an organization. In a way it serves as a rogue AP detection in the classic meaning too, as one can detect every not authorized AP around.

### Black and Whitelists

*Blacklists* are list of forbidden ESSIDs. There is no use in blacklisting BSSIDs as well, as differenciating between allowed BSSIDs should be done in white lists.

*Whitelists* are mappings of ESSIDs to a list of BSSIDs. Such, if a ESSID is on the allowed list, but the BSSID is not, this AP is not allowed. It is recommended to put ESSIDs of the whitelist on the blacklist as well, to ensure that every usage of this ESSID without allowed BSSID provokes an alert.

The Whitelist is organized as a hearing map, to ensure that only ESSID/BSSID combinations are allowed, which make sense regarding the physical location of a remote capture. Otherwise an attacker could use a valid ESSID/BSSID combination seen in an other room or building and use this to not get detected (see below for an example).

Both, black- and whitelists are yaml formatted text files. They are expected to be in the folder lists/whitelist.yml and lists/blacklist.yml.

Whitelists are scalars (ESSIDs) mapped to sequences (BSSIDs) which are mapped to sequences (interfaces), such as:

```
'ESSID1':
  'BSSID1':
  - 'AP1'
'ESSID2':
  'BSSID2':
  - 'AP1'
  - 'AP2'
  'BSSID3':
  - 'AP3'
...
```

Blacklists are just sequences of ESSIDs, such as:
```
- "ESSID1"
- "ESSID2"
```

### knownAP

Depending on the configuration new APs are saved to lists/knownAP.yml file. This is formatted the same way like a whitelist. Thus, it can be used after some time as a whitelist (training data, see option --train). It can be used to prevent that a unknown AP got mentioned multiple times as well.

## Fields of Log Messages

Key | Description of field | since version
----| -------------------- | -------------
version | Indicates the availability of fields as noted on this page | 1.0
name | Alert name | 1.0
text | Alert text | 1.0
reason | Reason for the message ('unknown' or 'blacklist') | 1.0
essid | SSID of captured frame | 1.0
bssid | BSSID of captured frame | 1.0
interface | Name of interface which captured data | 1.0
