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
import struct


def i80211_info(i80211, packet, off):

    if (i80211['type'][1] == 'Management'):
        return management(i80211, packet, off)

    if (i80211['type'][1] == 'Control'):
        return control(i80211, packet, off)
        
    return {}


def management(i80211, packet, off):

    if(i80211['subtype'][1] == 'Beacon' or 
       i80211['subtype'][1] == 'Probe Request' or 
       i80211['subtype'][1] == 'Probe Response'):
    
        elements = {
                'BSSID': i80211['addr3'],
                }
        elements.update(parse_element_fields(packet[off:]))
        return elements

    return {}


def control(i80211, packet, off):
    return {}

def parse_element_fields(stream):

    elements = {}
    offset = 12 # tagged fields

    while (offset < (len(stream)-1)):

        hdr_fmt = "<BB"
        hdr_len = struct.calcsize(hdr_fmt)
        elementID, length = struct.unpack_from(hdr_fmt, stream, offset)
        offset += hdr_len

        if (elementID == 0x00 and 'ESSID' not in elements):

            elements.update({
                'ESSID': (stream[offset:offset+length]).decode('utf-8', errors='replace'),
            })
            break; # TODO remove this break if you want to process more fields!!!

        offset += length + 2

    return elements 

