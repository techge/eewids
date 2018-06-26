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
    # https://github.com/techge/eewids/blob/master/doc/capture-fields.md
    # TODO

    if detected:

        # TODO 
        # create alert messages based on fields described on
        # https://github.com/techge/eewids/blob/master/doc/messages-fields.md
        # TODO
        alertname = 'SomethingTerrible'
        description = 'SomethingTerrible detected...'
        # TODO add additional fields if needed
        
        message = {
                'version': '1.0',
                'name': alertname,
                'text': description,
                'loglevel': 'alert',
                # TODO add additional fields if needed
                }

        return 'alert', message


def send_message(loglevel, message_cont, send_channel):

    message = json.dumps(message_cont)
    # TODO insert application name here!
    key = 'appname.' + loglevel

    send_channel.basic_publish(exchange='messages',
                               routing_key=key,
                               body=message)
    
    print(" [x] %r %r sent." % (loglevel, message_cont['text']))


def queue_bindings(channel, queue_name, exch):

    # TODO change exclusive to False if your detection method is scalable
    # that means it can get done by multiple instances
    # e.g. the app searches for suspicous fields in single frames and thus
    # doesn't need a holistic view of all frames seen
    channel.queue_declare(queue=queue_name, exclusive=True)

    # queue binding per frame type choosen above
    for frametype in type_table:

        routing_key = '*.' + frametype + '.*'
        channel.queue_bind(exchange=exch,
                           queue=queue_name,
                           routing_key=key)

    # queue binding per frame subtype choosen above
    for framesubtype in subtype_table:

        key = '*.*.' + framesubtype 
        channel.queue_bind(exchange=exch,
                           queue=queue_name,
                           routing_key=key)


def main(rab_host, rab_port):

    # sanity check, can be deleted after finishing the application
    if not type_table and not subtype_table:
        print("No frame type or subtype choosen, please adapt type tables to your needs!")
        sys.exit()

    # open Connection to RabbitMQ
    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)

    # open channel to consume capture
    recv_channel = connection.channel()

    # open channel to publish messages
    send_channel = connection.channel()

    send_channel.exchange_declare(exchange='messages',
                                  exchange_type='topic',
                                  durable=True,)

    # create queue and bind topics based on choosen types
    # TODO insert application name here!
    queue_bindings(recv_channel, 'appname', 'capture')

    def callback(ch, method, properties, body):

        # data arrived start the detection
        data = json.loads(body)
        loglevel, message_cont = detect_attack(data, options)

        if loglevel is not None:
            send_message(loglevel, message_cont, send_channel)

    recv_channel.basic_consume(callback,
    # TODO insert application name here!
                               queue='appname',
                               no_ack=True)

    print(' [*] Starting detection. To exit press CTRL+C')
    recv_channel.start_consuming()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Python template for creating awesome plugins for Eewids")

    parser.add_argument("--rabbit_host", default="rabbit-server",
                        help="host of RabbitMQ server", metavar="HOST")
    parser.add_argument("--rabbit_port", default="5672", 
                        help="port of RabbitMQ server", metavar="PORT")

    args = parser.parse_args()

    main(args.rabbit_host, args.rabbit_port)
