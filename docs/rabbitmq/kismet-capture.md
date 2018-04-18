Fields Submitted to Exchange "kismet_capture"
=============================================

This page tracks all information submitted to RabbitMQ on exchange 'kismet_capture'.

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

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
linktype | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Link layer type of the interface
snaplen | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | Mmaximum number of octets captured from each packet
if_name | pcapng: [IDB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_idb) | The name of the device used to capture data 
block_type | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) |  
length | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | 
interface_ID | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | Interface this packet comes from
time_high | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | upper 32 bits of a 64-bit timestamp
time_low | pcapng: [EPB](https://xml2rfc.tools.ietf.org/cgi-bin/xml2rfc.cgi?url=https://raw.githubusercontent.com/pcapng/pcapng/master/draft-tuexen-opsawg-pcapng.xml&modeAsFormat=html/ascii&type=ascii#section_epb) | lower 32 bits of a 64-bit timestamp 
TSFT | radiotap: [TSFT](http://www.radiotap.org/fields/TSFT.html) | Value in usec of the MAC’s 64-bit 802.11 Time Synchronization Function timer
flags | radiotap: [Flags](http://www.radiotap.org/fields/Flags.html) | Properties of transmitted and received frames
rate | radiotap: [Rate](http://www.radiotap.org/fields/Rate.html) | TX/RX data rate
chan_freq | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Tx/Rx frequency in MHz
chan_flags | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Channel flags
dbm_antsignal | radiotap: [Antenna Signal](http://www.radiotap.org/fields/dB%20antenna%20signal.html) | RF signal power at the antenna
rx_flags | radiotap: [RX Flags](http://www.radiotap.org/fields/RX%20flags.html) | Properties of received frames. 
antenna | radiotap: [Antenna](http://www.radiotap.org/fields/Antenna.html) | Unitless indication of the Rx/Tx antenna for this packet
fc | 80211 | Full frame control field 
protocol | 80211 | Protocol version (added for convenience) 
type | 80211 | Frame type (added for convenience) 
subtype | 80211 | Frame subtype (added for convenience) 
duration | 80211 | Duration field 
addr1 | 80211 | First address field 

The following information is situated in the radiotap header and the presence depends on the setup (e.g. the card's and clients capabilities etc.). If it is present it will be included too.

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
mcs_flags | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | Flags for MCS rate information
mcs_known | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) |
mcs_index | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | 
mcs_rate | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) |
ampdu_refnum | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | Frame received as part of an a-MPDU, ref number field
ampdu_flags | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) |
ampdu_delim_crc_val | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) |
ampdu_reserved | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) |

Below are frame specific fields.

## Management Frames
The following information is sent aditionally in case the captured frame was a management frame
(type == 'Management').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field
addr3 | 80211 | Third address field
seq | 80211 | Sequence number
frag | 80211 | Fragment number

### Beacon only
The following information is sent aditionally in case the captured frame was a Beacon frame
(subtype == 'Beacon').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
BSSID | 80211 | This is the same as 'addr3' and only for convenience
ESSID | 80211 | The SSID sent

## Control Frames
The following information is sent aditionally in case the captured frame was a Control frame
(type == 'Control').

### Block Ack only
The following information is sent aditionally in case the captured frame was a Block Ack frame
(type == 'Control' and subtype == 'Block Ack').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field 
ba_ctrl | 80211 | Block Ack control field 
ba_ssc | 80211 | Block Ack starting sequence control 
ba_bitmap | 80211 | Block Ack bitmap 

## Data Frames
The following information is sent aditionally in case the captured frame was a Data frame
(type == 'Data').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr2 | 80211 | Second address field 
addr3 | 80211 | Third address field 
seq | 80211 | Sequence number 
frag | 80211 | Fragment number 

### QoS data/QoS Null only
The following information is sent aditionally in case the captured frame was a QoS data or QoS Null frame
(type == 'Data' and (subtype == 'QoS data' or subtype == 'QoS Null').

Key | Belonging to layer | Description of field
----| ------------------ | --------------------
addr4 | 80211 | Forth address field
tid | 80211 | TID subfield
eosp | 80211 | End of service period (EOSP) subfield 
rspi | 80211 | Receiver service period initiated (RSPI) subfield 
mesh_ps | 80211 | Mesh power save level subfield 
