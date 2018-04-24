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
import pika
import json
import argparse


# TODO Choose the captured frame type, if you want to get *all* frames of this type (look below otherwise)
type_table = [

    #"Management",
    #"Control",
    #"Data",
    #"Extension",

    ]

# TODO Choose the captured frame subtype you want to get for your detection app by uncommenting here
subtype_table = [ 

    ## Management frames
    #"Association Request",
    #"Association Response",
    #"Reassociation Request",
    #"Reassociation Response",
    #"Probe Request",
    #"Probe Response",
    #"Timing Advertisment",
    #"Beacon",
    #"ATIM",
    #"Disassociation",
    #"Authentication",
    #"Deauthentication",
    #"Action",
    #"Action No Ack",

    ## Control frames
    #"Beamforming Report Poll",
    #"VHT NDP Announcement",
    #"Control Frame Extension",
    #"Control Wrapper",
    #"Block Ack Request",
    #"Block Ack",
    #"PS-Poll",
    #"RTS",
    #"CTS",
    #"ACK",
    #"CF-end",
    #"CF-end + CF-ack",

    ## Data frames
    #"Data",
    #"Data + CF-ack",
    #"Data + CF-poll",
    #"Data + CF-ack + CF-poll",
    #"Null",
    #"CF-ack",
    #"CF-poll",
    #"CF-ack + CF-poll",
    #"QoS data",
    #"QoS data + CF-ack",
    #"QoS data + CF-poll",
    #"QoS data + CF-ack + CF-poll",
    #"QoS Null",
    #"QoS + CF-poll (no data)",
    #"QoS + Cf-ack (no data)",

    ## Extension
    #"DMG Beacon",
    ]


def detect_attack(data):

    detected = False
    
    # TODO
    # This is the main part you have to think about. Here is your main code.
    # data is a python dictionary which contains all fields described on
    # https://github.com/techge/eewids/blob/master/docs/rabbitmq/kismet_capture-fields.md
    # TODO

    if detected:

        # TODO 
        # create alert messages based on fields described on
        # https://github.com/techge/eewids/blob/master/docs/rabbitmq/messages-fields.md
        # TODO
        alertname = 'SomethingTerrible'
        description = 'SomethingTerrible detected...'
        # ...
        
        alert = [
                'name': alertname
                'description': description
                # ...
                ]

        send_alert(alert)


def send_alert(alert):

    channel = connection.channel()
    channel.exchange_declare(exchange='messages',
                             exchange_type='topic')
    
    message = json.dumps(alert)

    # TODO adapt routing_key; format is servicename.messagetype
    # see https://github.com/techge/eewids/blob/master/docs/rabbitmq/messages-topics.md
    routing = 'app.alert' 
    channel.basic_publish(exchange='kismet_capture',
                          routing_key=routing,
                          body=message)
    
    print(" [x] Alert %r sent.", % message)
    connection.close()


def main(rab_host, rab_port):

    # sanity check
    if (!type_table and !subtype_table):
        print("No frame type or subtype choosen, please adapt type tables to your needs!")
        sys.exit()

    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='kismet_capture',
                             exchange_type='topic')

    # TODO change exclusive to False if your detection can get split between multiple workers
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # queue binding per frame type choosen above
    for key in type_table:

        routing_key = '*.' + key + '.*'
        channel.queue_bind('kismet_capture',
                           queue_name,
                           routing_key)

    # queue binding per frame subtype choosen above
    for key in subtype_table:

        routing_key = '*.*.' + key
        channel.queue_bind('kismet_capture',
                           queue_name,
                           routing_key)

    def callback(ch, method, properties, body):

        # data arrived begin the actual detection work in function above
        data = json.loads(body)
        detect_attack(data)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] Starting detection. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Python template for creating awesome plugins for Eewids")

    parser.add_argument("--rabbit_host", default="rabbit-server",
                        help="host of RabbitMQ server", metavar="HOST")
    parser.add_argument("--rabbit_port", default="5672", 
                        help="port of RabbitMQ server", metavar="PORT")

    args = parser.parse_args()

    main(args.rabbit_host, args.rabbit_port)
