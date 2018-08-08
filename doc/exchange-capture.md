Fields Submitted to Exchange "capture"
=============================================

This page tracks all information for topic exchange 'capture', which is used to publish all information to the packets captured.

*Note*: This information is still in constant change and not considered stable yet.

## Routing Keys

An application can create a RabbitMQ queue and bind it to the 'capture' exchange by using various routing keys. All parsed packets can be accessed by using the following routing key scheme:

    <interfaceID>.<frameType>.<frameSubtype>

The routing key for a Beacon frame captured by the interface with interfaceID '00000000' would read:

    00000000.Management.Beacon

Instead of binding a queue to every possible routing key, one is encouraged to use topics. This is done by using the asterisk symbol. Thus, to get all Beacon frames, one uses `*.*.Beacon`. To get all management frames of one specific interface, one subscribes to `interID.management.*` instead and so on.

More information on RabbitMQs exchange types (remember Eewids is using topic exchanges) can be found [here](https://www.cloudamqp.com/blog/2015-09-03-part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html).

## Fields Available for Captured Data

**Note**: Not every field is present in every data set. If an information is not available on a packet (e.g. a SSID does not exist for CTS frames) then it is not existence in the data published by RabbitMQ as well.

Key | Belonging to layer | Description of field | since version
----| ------------------ | -------------------- | -------------
version | EEWIDS | Indicates the availability of fields as noted on this page | 1.0
TSFT | radiotap: [TSFT](http://www.radiotap.org/fields/TSFT.html) | Value in usec of the MAC’s 64-bit 802.11 Time Synchronization Function timer | 1.0
flags | radiotap: [Flags](http://www.radiotap.org/fields/Flags.html) | Properties of transmitted and received frames | 1.0
rate | radiotap: [Rate](http://www.radiotap.org/fields/Rate.html) | TX/RX data rate | 1.0
chan_freq | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Tx/Rx frequency in MHz | 1.0
chan_flags | radiotap: [Channel](http://www.radiotap.org/fields/Channel.html) | Channel flags | 1.0
dbm_antsignal | radiotap: [Antenna Signal](http://www.radiotap.org/fields/dB%20antenna%20signal.html) | RF signal power at the antenna | 1.0
rx_flags | radiotap: [RX Flags](http://www.radiotap.org/fields/RX%20flags.html) | Properties of received frames.  | 1.0
antenna | radiotap: [Antenna](http://www.radiotap.org/fields/Antenna.html) | Unitless indication of the Rx/Tx antenna for this packet | 1.0
mcs_flags | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | Flags for MCS rate information | 1.0
mcs_known | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | | 1.0
mcs_index | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) |  | 1.0
mcs_rate | radiotap: [MCS](http://www.radiotap.org/fields/MCS.html) | | 1.0
ampdu_refnum | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | Frame received as part of an a-MPDU, ref number field | 1.0
ampdu_flags | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0
ampdu_delim_crc_val | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0
ampdu_reserved | radiotap: [A-MPDU](http://www.radiotap.org/fields/A-MPDU%20status.html) | | 1.0
wlan.fc | 80211 | Full frame control field  | 1.0
wlan.fc.version | 80211 | Protocol version | 1.0
wlan.fc.type | 80211 | Frame type | 1.0
wlan.fc.type.str | 80211 | Frame type (human-readable string, see [here](/doc/capture-topics.md#frame-typessubtypes))  | 1.0
wlan.fc.subtype | 80211 | Frame subtype | 1.0
wlan.fc.subtype.str | 80211 | Frame subtype (human-readable string, see [here](/doc/capture-topics.md#frame-typessubtypes))  | 1.0
wlan.duration | 80211 | Duration field  | 1.0
wlan.addr1 | 80211 | First address field  | 1.0
wlan.addr2 | 80211 | Second address field | 1.0
wlan.addr3 | 80211 | Third address field | 1.0
wlan.addr4 | 80211 | Forth address field | 1.0
wlan.seq | 80211 | Sequence number | 1.0
wlan.frag | 80211 | Fragment number | 1.0
wlan.ba.control | 80211 | Block Ack control field  | 1.0
wlan.ba.ssc | 80211 | Block Ack starting sequence control  | 1.0
wlan.ba.bm | 80211 | Block Ack bitmap  | 1.0
wlan.bssid | 80211 | This is the same as 'addr3' and only for convenience | 1.0
wlan.ssid | 80211 | The SSID sent | 1.0
wlan.country_info.code | 80211 | 
wlan.fixed.timestamp  | 80211 | 
wlan.fixed.beacon | 80211 | 
wlan.fixed.capabilities | 80211 | 
wlan.qos.tid | 80211 | TID subfield | 1.0
wlan.qos.eosp | 80211 | End of service period (EOSP) subfield  | 1.0
wlan.qos.rspi | 80211 | Receiver service period initiated (RSPI) subfield  | 1.0
wlan.mesh.config.cap.power_save_level | 80211 | Mesh power save level subfield  | 1.0

