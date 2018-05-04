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
import struct


def _parse_ssid(packet, length, offset):
    if length == 0:
        return {'ESSID': 'WILDCARD',}
    else:
        essid = (packet[offset:offset+length]).decode('utf-8', errors='replace')
        return {'ESSID': essid,} 

def _parse_country(packet, length, offset):
    code = packet[offset:offset+2].decode('ascii', errors='ignore')
    return {'country_code': code,} 

def _parse_default(packet, length, offset):
    return {} 

def _parse_fixed(packet):
    hdr_fmt = "<QHH"
    offset = struct.calcsize(hdr_fmt)
    ts, interval, capabilities = struct.unpack_from(hdr_fmt, packet, 0)

    return offset, {
            'i80211_ts': ts,
            'interval': interval,
            'capabilities': capabilities,
            }

def parse_element_fields(packet):

    if len(packet) < 12:
        return {}

    offset, elements = _parse_fixed(packet)

    while (offset < (len(packet)-2)):

        hdr_fmt = "<BB"
        hdr_len = struct.calcsize(hdr_fmt)
        elementID, length = struct.unpack_from(hdr_fmt, packet, offset)
        offset += hdr_len

        dispatch_table = {
                0x00: _parse_ssid,
                0x07: _parse_country,
                }

        new_elements = dispatch_table.get(elementID, _parse_default)(packet, length, offset)
        elements.update(new_elements)
        offset += length

    return elements 

