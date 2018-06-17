Fields Submitted to Exchange "capture"
=============================================

This page tracks all fields of messages submitted to RabbitMQ on exchange ['capture'](capture-topics.md).

*Note*: This information is still in constant change and not considered stable yet.

# Table of Contents

* [Always](#always)
* [Management Frames](#management-frames)
  * [Beacon only](#beacon-only)
* [Control Frames](#control-frames)
  * [Block Ack only](#block-ack-only)
* [Data Frames](#data-frames)
  * [QoS data/QoS Null only](#qos-dataqos-null-only)

## Always
The following table includes information which is logged for *every* frame sent to 'capture'.

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
version | EEWIDS | Indicates the availability of fields as noted on this page | 1.0
pcapng.linktype | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Link layer type of the interface | 1.0
pcapng.snaplen | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Mmaximum number of octets captured from each packet | 1.0
pcapng.if_name | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | The name of the device used to capture data  | 1.0
pcapng.if_ID | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | Interface this packet comes from | 1.0
pcapng.time_high | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | upper 32 bits of a 64-bit timestamp | 1.0
pcapng.time_low | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | lower 32 bits of a 64-bit timestamp  | 1.0
TSFT | radiotap: [TSFT](http://www.radiotap.org/fields/TSFT.html) | Value in usec of the MAC’s 64-bit 802.11 Time Synchronization Function timer | 1.0
flags | radiotap: [Flags](http://www.radiotap.org/fields/Flags.html) | Properties of transmitted and received frames | 1.0
rate | radiotap: [Rate](http://www.radiotap.org/fields/Rate.html) | TX/RX data rate | 1.0
chan_freq | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Tx/Rx frequency in MHz | 1.0
chan_flags | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Channel flags | 1.0
dbm_antsignal | radiotap: [Antenna Signal](http://www.radiotap.org/fields/dB%20antenna%20signal.html) | RF signal power at the antenna | 1.0
rx_flags | radiotap: [RX Flags](http://www.radiotap.org/fields/RX%20flags.html) | Properties of received frames.  | 1.0
antenna | radiotap: [Antenna](http://www.radiotap.org/fields/Antenna.html) | Unitless indication of the Rx/Tx antenna for this packet | 1.0
wlan.fc | 80211 | Full frame control field  | 1.0
wlan.fc.version | 80211 | Protocol version | 1.0
wlan.fc.type | 80211 | Frame type | 1.0
wlan.fc.type.str | 80211 | Frame type (human-readable string, see [here](/doc/capture-topics.md#frame-typessubtypes))  | 1.0
wlan.fc.subtype | 80211 | Frame subtype | 1.0
wlan.fc.subtype.str | 80211 | Frame subtype (human-readable string, see [here](/doc/capture-topics.md#frame-typessubtypes))  | 1.0
wlan.duration | 80211 | Duration field  | 1.0
wlan.addr1 | 80211 | First address field  | 1.0

The following information is situated in the radiotap header and the presence depends on the setup (e.g. the card's and clients capabilities etc.). If it is present it will be included too.

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
mcs_flags | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | Flags for MCS rate information | 1.0
mcs_known | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | | 1.0
mcs_index | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) |  | 1.0
mcs_rate | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | | 1.0
ampdu_refnum | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | Frame received as part of an a-MPDU, ref number field | 1.0
ampdu_flags | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0
ampdu_delim_crc_val | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0
ampdu_reserved | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0

Below are frame specific fields.

## Management Frames
The following information is sent aditionally in case the captured frame was a management frame
(wlan.type == 'Management') and the information was available.

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
wlan.addr2 | 80211 | Second address field | 1.0
wlan.addr3 | 80211 | Third address field | 1.0
wlan.seq | 80211 | Sequence number | 1.0
wlan.frag | 80211 | Fragment number | 1.0

### Additionall Information, availability depends on packet
Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
wlan.bssid | 80211 | This is the same as 'addr3' and only for convenience | 1.0
wlan.ssid | 80211 | The SSID sent | 1.0
wlan.country_info.code | 80211 | 
wlan.fixed.timestamp  | 80211 | 
wlan.fixed.beacon | 80211 | 
wlan.fixed.capabilities | 80211 | 

## Control Frames
The following information is sent aditionally in case the captured frame was a Control frame
(wlan.type == 'Control').

### Block Ack only
The following information is sent aditionally in case the captured frame was a Block Ack frame
(wlan.type == 'Control' and wlan.subtype == 'Block Ack').

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
wlan.addr2 | 80211 | Second address field  | 1.0
wlan.ba.control | 80211 | Block Ack control field  | 1.0
wlan.ba.ssc | 80211 | Block Ack starting sequence control  | 1.0
wlan.ba.bm | 80211 | Block Ack bitmap  | 1.0

## Data Frames
The following information is sent aditionally in case the captured frame was a Data frame
(wlan.type == 'Data').

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
wlan.addr2 | 80211 | Second address field  | 1.0
wlan.addr3 | 80211 | Third address field  | 1.0
wlan.seq | 80211 | Sequence number  | 1.0
wlan.frag | 80211 | Fragment number  | 1.0

### QoS data/QoS Null only
The following information is sent aditionally in case the captured frame was a QoS data or QoS Null frame
(wlan.type == 'Data' and (wlan.subtype == 'QoS data' or wlan.subtype == 'QoS Null').

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
wlan.addr4 | 80211 | Forth address field | 1.0
wlan.qos.tid | 80211 | TID subfield | 1.0
wlan.qos.eosp | 80211 | End of service period (EOSP) subfield  | 1.0
wlan.qos.rspi | 80211 | Receiver service period initiated (RSPI) subfield  | 1.0
wlan.mesh.config.cap.power_save_level | 80211 | Mesh power save level subfield  | 1.0
