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
import json
import pika

# debugging TODO remove in production
from scapy.all import hexdump


def parse(packet):

    off, radiotap = radiotap_parse(packet)
    off, i80211 = ieee80211_parse(packet, off)
    i80211_detail = i80211_info(i80211, packet, off)
    parsed = radiotap
    parsed.update(i80211)
    parsed.update(i80211_detail)

    return parsed


def main(kis_host, kis_port, kis_user, kis_pass, rab_host):

    s = requests.Session()
    s.auth = (kis_user, kis_pass)
    s.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 
    
    url = kis_host + ':' + kis_port + '/pcap/all_packets.pcapng'
    r = s.get(url, stream=True) # start pcapng stream
    
    stream = b'' # buffer for stream data
    interface_description = {}
    package = 0 # just temporary counting TODO remove in production

    # we always grap 4 octets at once, as pcapng pads blocks to 32bit
    for line in r.iter_content(chunk_size=4): 

        # filter out keep-alive new lines
        if line:

            stream = stream + line 
            blocksize = block_total_length(stream)

            # we have a complete block and can start analyzing
            if (blocksize > 0 and len(stream) >= blocksize): 

                #print(hexdump(stream[:blocksize]), "\r\n") # TODO remove in production

                packet, block_information = block_processing(stream)

                # update interface_description
                if (block_information['block_type'][1] == 'Interface Description Block'):
                    interface_description = {
                            'linktype': block_information['linktype'],
                            'snaplen': block_information['snaplen'],
                            'if_name': block_information['if_name'].decode('utf-8'),
                            }

                # actual packet arrived, parsing and processing
                if (packet != None):

                    cap_info = interface_description
                    cap_info.update(block_information)
                    cap_info.update(parse(packet))

                    #print (cap_info) #  TODO remove in production

                    if(cap_info.get('ESSID') != None):

                        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rab_host))
                        channel = connection.channel()

                        channel.queue_declare(queue='hello')

                        message = json.dumps(cap_info)

                        channel.basic_publish(exchange='',
                                              routing_key='hello',
                                              body=message)
                        print(" [x] Sent ",message)
                        connection.close()

                package += 1 #  TODO remove in production
                #print("Package ", package, "\r\n\r\n") # TODO remove in production
                stream = stream[blocksize:] # make nothing gets lost, should always result in empty string though

            #if (package == 5): # TODO remove in production
            #    break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process Kismet's pcapng stream and sends it to RabbitMQ")

    parser.add_argument("--kismet_host", default="http://localhost", 
                        help="host of Kismet server", metavar="HOST")
    parser.add_argument("--kismet_port", default="2501", 
                        help="port of Kismet server", metavar="PORT")
    parser.add_argument("--kismet_user", default="kismet", 
                        help="username for Kismet server", metavar="USER")
    parser.add_argument("--kismet_pass", default="kismet", 
                        help="password for Kismet server", metavar="PASS")
    parser.add_argument("--rabbit_host", default="localhost",
                        help="host of RabbitMQ server", metavar="HOST")

    args = parser.parse_args()

    if (args.kismet_host[0:4] != "http"):
        args.kismet_host = "http://" + args.kismet_host

    main(args.kismet_host, args.kismet_port, args.kismet_user, args.kismet_pass, args.rabbit_host)
