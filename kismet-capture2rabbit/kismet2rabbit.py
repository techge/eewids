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
import json
import pika
import requests
from i80211_detail import i80211_info
from pcapng import block_total_length, block_processing 
from radiotap import radiotap_parse, ieee80211_parse


def parse(packet):

    off, radiotap = radiotap_parse(packet)
    off, i80211 = ieee80211_parse(packet, off)
    i80211_detail = i80211_info(i80211, packet, off)
    parsed = radiotap
    parsed.update(i80211)
    parsed.update(i80211_detail)

    return parsed


def distribute(cap_info, rab_host, rab_port):

    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                           port=rab_port,
                                           connection_attempts=5)
    connection = pika.BlockingConnection(ConnectionParameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='kismet_capture',
                             exchange_type='topic')
    
    message = json.dumps(cap_info)

    # routing_key is if_name.type.subtype 
    routing = cap_info['if_name'] + '.' + cap_info['type'][1] + '.' + cap_info['subtype'][1]
    channel.basic_publish(exchange='kismet_capture',
                          routing_key=routing,
                          body=message)
    
    print(" [x] Sent ",message)
    connection.close()


def main(kis_host, kis_port, kis_user, kis_pass, rab_host, rab_port):

    s = requests.Session()
    s.auth = (kis_user, kis_pass)
    s.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 
    
    url = kis_host + ':' + kis_port + '/pcap/all_packets.pcapng'
    r = s.get(url, stream=True) # start pcapng stream
    
    stream = b'' # buffer for stream data
    interface_description = {}

    # we always grap 4 octets at once, as pcapng pads blocks to 32bit
    for line in r.iter_content(chunk_size=4): 

        # filter out keep-alive new lines
        if line:

            stream = stream + line 
            blocksize = block_total_length(stream)

            # we have a complete block and can start analyzing
            if (blocksize > 0 and len(stream) >= blocksize): 

                packet, block_information = block_processing(stream)

                # update interface_description
                if (block_information['block_type'][1] == 'Interface Description Block'):
                    interface_description = {
                            'linktype': block_information['linktype'],
                            'snaplen': block_information['snaplen'],
                            'if_name': block_information['if_name'].decode('utf-8'),
                            }

                # actual packet arrived, parsing and distributing 
                if (packet != None):

                    cap_info = interface_description
                    cap_info.update(block_information)
                    cap_info.update(parse(packet))

                    distribute(cap_info, rab_host, rab_port)

                stream = stream[blocksize:] # make sure nothing gets lost, should always result in empty string though


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
    parser.add_argument("--rabbit_port", default="5672", 
                        help="port of RabbitMQ server", metavar="PORT")

    args = parser.parse_args()

    if (args.kismet_host[0:4] != "http"):
        args.kismet_host = "http://" + args.kismet_host

    main(args.kismet_host, args.kismet_port, args.kismet_user, args.kismet_pass, args.rabbit_host, args.rabbit_port)
