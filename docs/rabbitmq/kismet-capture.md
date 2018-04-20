Fields Submitted to Exchange "kismet_capture"
=============================================

This page tracks all information submitted to RabbitMQ on exchange 'kismet_capture'.

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
The following table includes information which is logged for *every* frame sent to 'kismet_capture'.

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
version | EEWIDS | Indicates the availability of fields as noted on this page | 1.0
linktype | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Link layer type of the interface | 1.0
snaplen | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Mmaximum number of octets captured from each packet | 1.0
if_name | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | The name of the device used to capture data  | 1.0
block_type | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) |   | 1.0
length | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) |  | 1.0
interface_ID | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | Interface this packet comes from | 1.0
time_high | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | upper 32 bits of a 64-bit timestamp | 1.0
time_low | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | lower 32 bits of a 64-bit timestamp  | 1.0
TSFT | radiotap: [TSFT](http://www.radiotap.org/fields/TSFT.html) | Value in usec of the MAC’s 64-bit 802.11 Time Synchronization Function timer | 1.0
flags | radiotap: [Flags](http://www.radiotap.org/fields/Flags.html) | Properties of transmitted and received frames | 1.0
rate | radiotap: [Rate](http://www.radiotap.org/fields/Rate.html) | TX/RX data rate | 1.0
chan_freq | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Tx/Rx frequency in MHz | 1.0
chan_flags | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Channel flags | 1.0
dbm_antsignal | radiotap: [Antenna Signal](http://www.radiotap.org/fields/dB%20antenna%20signal.html) | RF signal power at the antenna | 1.0
rx_flags | radiotap: [RX Flags](http://www.radiotap.org/fields/RX%20flags.html) | Properties of received frames.  | 1.0
antenna | radiotap: [Antenna](http://www.radiotap.org/fields/Antenna.html) | Unitless indication of the Rx/Tx antenna for this packet | 1.0
fc | 80211 | Full frame control field  | 1.0
protocol | 80211 | Protocol version (added for convenience)  | 1.0
type | 80211 | Frame type (added for convenience)  | 1.0
subtype | 80211 | Frame subtype (added for convenience)  | 1.0
duration | 80211 | Duration field  | 1.0
addr1 | 80211 | First address field  | 1.0

The following information is situated in the radiotap header and the presence depends on the setup (e.g. the card's and clients capabilities etc.). If it is present it will be included too.

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
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
(type == 'Management').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field | 1.0
addr3 | 80211 | Third address field | 1.0
seq | 80211 | Sequence number | 1.0
frag | 80211 | Fragment number | 1.0

### Beacon only
The following information is sent aditionally in case the captured frame was a Beacon frame
(subtype == 'Beacon').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
BSSID | 80211 | This is the same as 'addr3' and only for convenience | 1.0
ESSID | 80211 | The SSID sent | 1.0

## Control Frames
The following information is sent aditionally in case the captured frame was a Control frame
(type == 'Control').

### Block Ack only
The following information is sent aditionally in case the captured frame was a Block Ack frame
(type == 'Control' and subtype == 'Block Ack').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field  | 1.0
ba_ctrl | 80211 | Block Ack control field  | 1.0
ba_ssc | 80211 | Block Ack starting sequence control  | 1.0
ba_bitmap | 80211 | Block Ack bitmap  | 1.0

## Data Frames
The following information is sent aditionally in case the captured frame was a Data frame
(type == 'Data').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field  | 1.0
addr3 | 80211 | Third address field  | 1.0
seq | 80211 | Sequence number  | 1.0
frag | 80211 | Fragment number  | 1.0

### QoS data/QoS Null only
The following information is sent aditionally in case the captured frame was a QoS data or QoS Null frame
(type == 'Data' and (subtype == 'QoS data' or subtype == 'QoS Null').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr4 | 80211 | Forth address field | 1.0
tid | 80211 | TID subfield | 1.0
eosp | 80211 | End of service period (EOSP) subfield  | 1.0
rspi | 80211 | Receiver service period initiated (RSPI) subfield  | 1.0
mesh_ps | 80211 | Mesh power save level subfield  | 1.0
