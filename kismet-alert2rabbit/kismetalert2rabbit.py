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
import sched, time


def distribute(data, rab_host, rab_port):

    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=5)
    connection = pika.BlockingConnection(ConnectionParameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='alerts',
                             exchange_type='direct')

    message = json.dumps(data)

    channel.basic_publish(exchange='alerts',
                          routing_key='kismet_alerts',
                          body=message)

    print(" [x] Sent Alert %s: %s " % (data['kismet.alert.header'], data['kismet.alert.text']))
    connection.close()


def main(kis_host, kis_port, kis_user, kis_pass, rab_host, rab_port):

    sess = requests.Session()
    sess.auth = (kis_user, kis_pass)
    sess.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 

    # we need to request alerts periodically
    # using 'sched' Event Scheduler to request every 10 seconds
    sc = sched.scheduler(time.time, time.sleep)
    TS = '0.0' # Kismet timestamp, needed for URL

    # this is the part repeated periodically by scheduler
    def request_alerts(sched, TS): 

        url = kis_host + ':' + kis_port + '/alerts/last-time/' + str(TS) + '/alerts.json'
        r = sess.get(url)

        TS = r.json()['kismet.alert.timestamp'] # TS for next tick
        alertlist = r.json()['kismet.alert.list'] # that's what we came for...

        if alertlist:
            for k in alertlist: 
                distribute(k, rab_host, rab_port)

        sc.enter(10, 1, request_alerts, (sched, TS))

    # actually start scheduler
    sc.enter(10, 1, request_alerts, (sc, TS))
    sc.run()



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
