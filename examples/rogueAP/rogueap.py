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
import yaml
import os.path


type_table = [

    #"Management",
    #"Control",
    #"Data",
    #"Extension",

    ]

subtype_table = [ 

    ## Management frames
    #"Association Request",
    #"Association Response",
    #"Reassociation Request",
    #"Reassociation Response",
    #"Probe Request",
    "Probe Response",
    #"Timing Advertisment",
    "Beacon",
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


def load_yml(path):

    if os.path.exists(path):

        with open(path, "r") as f:
            try:
                aps = yaml.load(f)
            except yaml.YAMLError as exc:
                print(exc)
            f.close()
        return aps

    return {}


def write_yml(path, data):

    with open(path, "w") as f:

        try:
            yaml.dump(data, f, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        f.close()


def on_whitelist(essid, bssid):

    aps = load_yml("lists/whitelist.yml")

    if aps.get(essid): # essid exists in list
        if bssid in aps[essid]:
            return True 

    return False

def on_blacklist(essid):

    aps = load_yml("lists/blacklist.yml")

    if essid in aps:
        return True

    return False


def save_new_ap(essid, bssid):
    """
    Saves ESSID:BSSID combination to knownAP.yml file.
    
    Returns True if new AP was seen and saved.
    Returns False if AP was already known.
    """

    aps = load_yml("lists/knownAP.yml")

    # check existence
    if aps.get(essid): # essid exists in list
        if bssid in aps[essid]:
            return False 
        else:
            aps[essid].append(bssid) # add bssid
    else:
        aps.update({essid: [bssid],}) # add essid/bssid

    write_yml("lists/knownAP.yml", aps)

    return True


def detect_rogueap(data, options):

    essid = data['ESSID']
    bssid = data['BSSID']

    message = {
            'name': 'RogueAP',
            'description': 'Access point (%s - %s)' % (essid, bssid),
            }

    if on_whitelist(essid, bssid):

        return None, None

    if on_blacklist(essid):

        message['description'] = message['description'] + ' on blacklist!'
        message.update({'reason': 'blacklist',})
        return 'alert', message
    
    else:

        message['description'] = message['description'] + ' unknown'
        message.update({'reason': 'unknown',})

        # if option '--alert' is used, we don't care about knownAPs!
        if options.get('alert'):
            return 'alert', message

        # save new APs if not on knownAP list
        if options.get('train'):

            if not save_new_ap(essid, bssid): # AP already known
                return None, None

        # send message
        if options.get('info'):
            return 'info', message
        else:
            return 'warning', message


def send_message(messagetype, message_cont, send_channel):

    message = json.dumps(message_cont)
    key = 'rogueap.' + messagetype

    send_channel.basic_publish(exchange='messages',
                               routing_key=key,
                               body=message)
    
    print(" [x] %r %r sent." % (messagetype, message_cont['description']))


def main(rab_host, rab_port, options):

    # open Connection to RabbitMQ
    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)

    # open channel to consume kismet capture
    recv_channel = connection.channel()
    recv_channel.exchange_declare(exchange='kismet_capture',
                                  exchange_type='topic')

    # open channel to publish alerts
    send_channel = connection.channel()
    send_channel.exchange_declare(exchange='messages',
                                  exchange_type='topic')

    result = recv_channel.queue_declare(exclusive=False)
    queue_name = result.method.queue

    # queue binding per frame type choosen above
    for frametype in type_table:

        routing_key = '*.' + frametype + '.*'
        recv_channel.queue_bind(exchange='kismet_capture',
                           queue=queue_name,
                           routing_key=key)

    # queue binding per frame subtype choosen above
    for framesubtype in subtype_table:

        key = '*.*.' + framesubtype 
        recv_channel.queue_bind(exchange='kismet_capture',
                           queue=queue_name,
                           routing_key=key)

    def callback(ch, method, properties, body):

        # data arrived start the detection
        data = json.loads(body)
        messagetype, message_cont = detect_rogueap(data, options)
        if messagetype is not None:
            send_message(messagetype, message_cont, send_channel)

    recv_channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] Starting detection. To exit press CTRL+C')
    recv_channel.start_consuming()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Rogue access point detection for Eewids. Store your whitelist.yml and/or blacklist.yml in folder 'lists', if needed.")

    parser.add_argument("--rabbit_host", default="rabbit-server",
                        help="Host of RabbitMQ server", metavar="HOST")
    parser.add_argument("--rabbit_port", default="5672", 
                        help="Port of RabbitMQ server", metavar="PORT")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--alert", action="store_true", help="Send alerts for access points not on whitelist (instead of warnings). Note that blacklist members will always provoke an alert. Thus, this option is for whitelist enforcement and this option can not get combined with --train.")
    group.add_argument("--train", action="store_true", help="Create/use knownAP.yml of already seen access points. If this flag is used, only access points never seen before provoke a warning.")
    parser.add_argument("--info", action="store_true", help="Send info instead of warning. Blacklist members will always provoke an alert though.")

    args = parser.parse_args()

    options = {
            'alert': args.alert,
            'info': args.info,
            'train': args.train,
            }

    main(args.rabbit_host, args.rabbit_port, options)
