#!/usr/bin/python

'''
    This file is part of EEWIDS (Easily Expandable WIDS)

    Copyright (C) 2018 Alexander Paetzelt <techge+eewids posteo net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys
import argparse
import json
import parser as p
import pika
import requests
from pcapng import block_total_length, block_processing 


def distribute(cap_info, channel):

    message = json.dumps(cap_info)

    # routing_key is pcapng.if_name.type.subtype 
    key = cap_info['pcapng.if_name'] + '.' + cap_info['wlan.fc.type.str'] + '.' + cap_info['wlan.fc.subtype.str']
    channel.basic_publish(exchange='capture',
                          routing_key=key,
                          body=message)

    print(" [x] Sent ",message)


def main(kis_host, kis_port, kis_user, kis_pass, rab_host, rab_port):

    # connection to Kismet server
    s = requests.Session()
    s.auth = (kis_user, kis_pass)
    s.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 

    url = kis_host + ':' + kis_port + '/pcap/all_packets.pcapng'
    r = s.get(url, stream=True) # start pcapng stream

    # connection to RabbitMQ
    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='capture',
                             exchange_type='topic',
                             durable=True,)

    # initializing vars
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
                            'pcapng.linktype': block_information['pcapng.linktype'],
                            'pcapng.snaplen': block_information['pcapng.snaplen'],
                            'pcapng.if_name': block_information['pcapng.if_name'].decode('utf-8'),
                            }

                # actual packet arrived, parsing and distributing 
                if (packet != None):

                    cap_info = interface_description
                    cap_info.update(block_information)
                    cap_info.pop('block_type')
                    cap_info.pop('length')
                    cap_info.update(p.packet_parse(packet))

                    distribute(cap_info, channel)

                stream = stream[blocksize:] # make sure nothing gets lost, should always result in empty string though

    connection.close()

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
