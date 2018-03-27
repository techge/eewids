#!/usr/bin/python

'''
This file is part of EEWIDS 

EEWIDS is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

EEWIDS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import sys
import argparse
import requests
from pcapng import block_total_length, block_processing 
from radiotap import radiotap_parse, ieee80211_parse
from i80211_detail import i80211_info
import pika
#from influxdb import InfluxDBClient

# debugging
from scapy.all import hexdump


def main(kis_host, kis_port, kis_user, kis_pass):

    s = requests.Session()
    s.auth = (kis_user, kis_pass)
    s.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 
    
    url = kis_host + ':' + kis_port + '/pcap/all_packets.pcapng'
    r = s.get(url, stream=True) # start pcapng stream
    
    stream = b'' # buffer for stream data
    interface_description = {}
    package = 0 # just temporary counting

    # we always grap 4 octets at once, as pcapng pads blocks to 32bit
    for line in r.iter_content(chunk_size=4): 

        # filter out keep-alive new lines
        if line:

            stream = stream + line 
            blocksize = block_total_length(stream)

            # we have a complete block and can start analyzing
            if (blocksize > 0 and len(stream) >= blocksize): 

                print(hexdump(stream[:blocksize]), "\r\n")

                packet, block_information = block_processing(stream)

                if (block_information['block_type'][1] == 'Interface Description Block'):
                    interface_description = {
                            'linktype': block_information['linktype'],
                            'snaplen': block_information['snaplen'],
                            'if_name': block_information['if_name'],
                            }

                if (packet != None):

                    off, radiotap = radiotap_parse(packet)
                    off, i80211 = ieee80211_parse(packet, off)
                    i80211_detail = i80211_info(i80211, packet, off)
                    cap_info = interface_description
                    cap_info.update(block_information)
                    cap_info.update(radiotap)
                    cap_info.update(i80211)
                    cap_info.update(i80211_detail)
                    
                    #print (cap_info)

                    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                    channel = connection.channel()

                    channel.queue_declare(queue='hello')

                    channel.basic_publish(exchange='',
                                          routing_key='hello',
                                          body='Hello World!')
                    print(" [x] Sent 'Hello World!'")
                    connection.close()

                package += 1
                #print("Package ", package, "\r\n\r\n")
                stream = stream[blocksize:]

            if (package == 5):
                break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process Kismet's pcapng stream and sends it to Apache Kafka")

    parser.add_argument("--kis_host", default="http://localhost", 
                        help="host of kismet server", metavar="HOST")
    parser.add_argument("--kis_port", default="2501", 
                        help="port of kismet server", metavar="PORT")
    parser.add_argument("--kis_user", default="kismet", 
                        help="username for kismet server", metavar="USER")
    parser.add_argument("--kis_pass", default="kismet", 
                        help="password for kismet server", metavar="PASS")

    args = parser.parse_args()

    if (args.kis_host[0:4] != "http"):
        args.kis_host = "http://" + args.kis_host

    main(args.kis_host, args.kis_port, args.kis_user, args.kis_pass)
