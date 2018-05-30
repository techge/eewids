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


def on_whitelist(essid, bssid, if_name):

    aps = load_yml("lists/whitelist.yml")

# TODO don't see why we shouldn't test at once (last if-clause)
# probably fails, if essid not in there -> maybe there is still a more elegant way
    if aps.get(essid): # essid exists in list
        if bssid in aps[essid]:
            if if_name in aps[essid][bssid]:
                return True 

    return False

def on_blacklist(essid):

    aps = load_yml("lists/blacklist.yml")

    if essid in aps:
        return True

    return False


def save_new_ap(essid, bssid, if_name):
    """
    Saves ESSID:BSSID:if_name combination to knownAP.yml file.
    
    Returns True if new AP was seen and saved.
    Returns False if AP was already known.
    """

    aps = load_yml("lists/knownAP.yml")

    # check existence
    if aps.get(essid): # essid exists in list
        if bssid in aps[essid]:
            if if_name in aps[essid][bssid]:
                return False 
            else:
                aps[essid][bssid].append(if_name)   # add if_name
        else:
            aps[essid].update({bssid: [if_name],})  # add bssid,if_name
    else:
        aps.update({essid: {bssid: [if_name],},})   # add essid,bssid,if_name
        # TODO Is this working for every three cases? Is it overriding anything?

#TODO this is not save for multi-container! load and update in one step;
# ensure idem potence!
    write_yml("lists/knownAP.yml", aps)

    return True


def detect_rogueap(data, options):

    essid = data['wlan.ssid']
    bssid = data['wlan.bssid']
    if_name = data['pcapng.if_name']

    message = {
            'version': '1.0',
            'name': 'RogueAP',
            'text': 'Access point (%s - %s)' % (essid, bssid),
            'essid': essid,
            'bssid': bssid,
            'interface': if_name,
            }

    if on_whitelist(essid, bssid, if_name):

        return None, None

    if on_blacklist(essid):

        message['text'] = message['text'] + ' on blacklist!'
        message.update({'reason': 'blacklist',})
        return 'alert', message
    
    message['text'] = message['text'] + ' unknown to ' + if_name
    message.update({'reason': 'unknown',})

    # if option '--alert' is used, we don't care about knownAPs!
    if options.get('alert'):
        return 'alert', message

    # save new APs if not on knownAP list
    if options.get('train'):

        if not save_new_ap(essid, bssid, if_name): # AP already known
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
    
    print(" [x] %r %r sent." % (messagetype, message_cont['text']))


def queue_bindings(channel, queue_name, exch):

    channel.queue_declare(queue=queue_name, exclusive=False)

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


def main(rab_host, rab_port, options):

    # open Connection to RabbitMQ
    ConnectionParameters = pika.ConnectionParameters(host=rab_host,
                                                     port=rab_port,
                                                     connection_attempts=10)
    connection = pika.BlockingConnection(ConnectionParameters)

    # open channel to consume kismet capture
    recv_channel = connection.channel()

    # open channel to publish alerts
    send_channel = connection.channel()

    # create queue and bind topics based on choosen types
    # TODO I think you may should check if already existence
    # I don't know for sure, if binding routing keys for 
    # already existing queue is a problem
    queue_bindings(recv_channel, 'rogueap', 'kismet_capture')

    def callback(ch, method, properties, body):

        # data arrived start the detection
        data = json.loads(body)
        messagetype, message_cont = detect_rogueap(data, options)

        if messagetype is not None:
            send_message(messagetype, message_cont, send_channel)

    recv_channel.basic_consume(callback,
                               queue='rogueap',
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
