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
import requests


def main(kis_host, kis_port, kis_user, kis_pass, alertname, alerttext):

    sess = requests.Session()
    sess.auth = (kis_user, kis_pass)
    sess.get(kis_host + ':' + kis_port + '/session/check_session') # authenticate with kismet server 
    url = kis_host + ':' + kis_port + '/alerts/raise_alert.cmd'
    
    payload = {
            'name': alertname,
            'text': alerttext,
            }

    pd = json.dumps(payload)

    jd = {
            'json': pd
         }

    r = sess.post(url, data=jd)

    print(r.text)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Raise Kismet alert")

    parser.add_argument("--kismet_host", default="http://localhost", 
                        help="host of Kismet server", metavar="HOST")
    parser.add_argument("--kismet_port", default="2501", 
                        help="port of Kismet server", metavar="PORT")
    parser.add_argument("--kismet_user", default="kismet", 
                        help="username for Kismet server", metavar="USER")
    parser.add_argument("--kismet_pass", default="kismet", 
                        help="password for Kismet server", metavar="PASS")
    parser.add_argument("-n", "--name", default="SOURCEERROR", help="alert name of alert you want to raise", metavar="NAME")
    parser.add_argument("-t", "--text", default="Testalert", 
                        help="alert text of alert you want to raise", metavar="TEXT")

    args = parser.parse_args()

    if (args.kismet_host[0:4] != "http"):
        args.kismet_host = "http://" + args.kismet_host

    main(args.kismet_host, args.kismet_port, args.kismet_user, args.kismet_pass, args.name, args.text)
