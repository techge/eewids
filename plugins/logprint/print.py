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


import pika
import json
import argparse


def main(rab_host, rab_port):

    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='messages',
                             exchange_type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='messages',
                       queue=queue_name,
                       routing_key='*.*')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("Message arrived: App %r: %r" % (data['name'], data['text']))
        print(data)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Print Beacons captured by Eewids")

    parser.add_argument("--rabbit_host", default="rabbit-server",
                        help="host of RabbitMQ server", metavar="HOST")
    parser.add_argument("--rabbit_port", default="5672", 
                        help="port of RabbitMQ server", metavar="PORT")

    args = parser.parse_args()

    main(args.rabbit_host, args.rabbit_port)
