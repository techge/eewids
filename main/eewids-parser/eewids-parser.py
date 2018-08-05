#!/usr/bin/env python

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
import pika
import requests

import parser as p


# TODO don't like the function name, make it more appropiate
def distribute(cap_info, channel):

    message = json.dumps(cap_info)

    # routing_key is pcapng.if_name.type.subtype 
    # TODO need if_name or a similiar disctinction
    key = 'if_name' + '.' + cap_info['wlan.fc.type.str'] + '.' + cap_info['wlan.fc.subtype.str']
    channel.basic_publish(exchange='capture',
                          routing_key=key,
                          body=message)

    print(" [x] Sent ",message)


def main(rab_host, rab_port):

    # open connection to RabbitMQ
    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)

    # open channel to consume raw capture data
    recv_channel = connection.channel()

    # open channel to publish parsed capture data 
    send_channel = connection.channel()

    # declare exchange
    # TODO maybe you need to check if it already exists!
    send_channel.exchange_declare(exchange='capture',
                                  exchange_type='topic',
                                  durable=True,)

    # create queue for receiving raw capture data
    # TODO you probably do not want a random queue, but one which is used by multiple workers!!!
    recv_channel.queue_declare(queue='eewids-parser', exclusive=False)
    #recv_queue = recv_channel.queue.declare(exclusive=True)
    # TODO change routing key on capture tool and here, make it meaningful and global/as argument
    recv_channel.queue_bind(exchange='capture-raw', queue='eewids-parser', routing_key='*.*.*')

    def callback(ch, method, properties, body):

        parsed_data = p.packet_parse(body)
        distribute(parsed_data, send_channel)

    # TODO look up right arguments to make sure that this is dividable through multiple workers!
    recv_channel.basic_consume(callback,
                               queue='eewids-parser',
                               no_ack=False)

    print(' [*] Starting parsing. To exit press CTRL+C')
    recv_channel.start_consuming()

    connection.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Parse raw capture data and send it to RabbitMQ")

    parser.add_argument("--rabbit_host", default="localhost",
                        help="host of RabbitMQ server", metavar="HOST")
    parser.add_argument("--rabbit_port", default="5672", 
                        help="port of RabbitMQ server", metavar="PORT")

    args = parser.parse_args()

    main(args.rabbit_host, args.rabbit_port)
