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


def block_total_length(stream):
    """ Returns the size (in Bytes) of next block in stream as saved in Block Total Length field

    Value is 0 if no complete block is included in stream yet
    """

    if (len(stream) >= 8):

        length, = struct.unpack_from("<I", stream, 4)
        return length

    return 0


def block_processing(stream):
    """ Return block type and information found in block
    """
    
    if (stream[0:4] == b'\n\r\r\n'):
        return block_section_header(stream)

    if (stream[0:4] == b'\x01\x00\x00\x00'):
        return block_interface_description(stream)
    
    if (stream[0:4] == b'\x06\x00\x00\x00'):
        return block_enhanced(stream)

    else:
        print("\r\nUnknown Block Type. Skipping.")
        return None, None


def block_section_header(stream):

    hdr_fmt = "<IIIHH"
    block, length, by_ord, maj_ver, min_ver = struct.unpack_from(hdr_fmt, stream, 0)

    block_information = {
        'block_type':   (0, 'Section Header Block'),
        'length':       length,
        'byteorder':    by_ord,
        'major_ver':    maj_ver,
        'minor_ver':    min_ver,
    }

    # TODO read option fields (not used by Kismet though)

    end_length, = struct.unpack_from("<I", stream, length - 4)
    if (length != end_length):
        print("Warning: Section Header Block broken\r\n",
              "first and second total length field do not match")

    return None, block_information


def block_interface_description(stream):

    hdr_fmt = "<IIHHI"
    block, length, linktype, reserved, snaplen = struct.unpack_from(hdr_fmt, stream, 0)

    block_information = {
        'block_type':       (1, 'Interface Description Block'),
        'length':           length,
        'pcapng.linktype':  linktype,
        #'reserved':         reserved,
        'pcapng.snaplen':   snaplen,
    }

    end_length, = struct.unpack_from("<I", stream, length - 4)
    if (length != end_length):
        print("Warning: Interface Description Block broken\r\n",
              "first and second total length field do not match")

    optionbyte = 16

    # processing option fields
    # TODO there are a lot more option fields, but they does not seem to be used by Kismet
    # -> ignoring for now
    while (optionbyte < length - 4):
        
        code, op_len = struct.unpack_from("<HH", stream, optionbyte)
        
        # if_name option field
        if (code == 2):
            block_information.update({
                'pcapng.if_name': stream[optionbyte + 4:optionbyte + 4 + op_len],
            })

        if (code == 3):
            block_information.update({
                'pcapng.if_description': stream[optionbyte + 4:optionbyte + 4 + op_len],
            })

        # end of option fields
        if (code == 0):
            break

        padding = 4 - op_len%4 
        optionbyte = optionbyte + 4 + op_len + padding

    return None, block_information


def block_enhanced(stream):

    hdr_fmt = "<IIIIIII"
    data_start = struct.calcsize(hdr_fmt)
    block, length, iID, timeh, timel, cap_len, orig_len = struct.unpack_from(hdr_fmt, stream, 0)
    
    block_information = {
        'block_type':              (6, 'Enhanced Packet Block'),
        'length':                  length,
        'pcapng.if_ID':            iID, 
        'pcapng.time_high':        timeh,
        'pcapng.time_low':         timel,
        'pcapng.cap_pack_len':     cap_len,
        'pcapng.orig_pack_len':    orig_len,
    }

    end_length, = struct.unpack_from("<I", stream, length - 4)
    if (length != end_length):
        print("Warning: Enhanced Packet Block broken\r\n",
              "first and second total length field do not match")

    if (cap_len != orig_len): 
        print("Warning: Packet was not captured completey!")

    # TODO parse option fields, probably not used by Kismet though
    # (stream[data_start + cap_len:enddata]

    # package cleaned of pcap-ng stuff
    data = stream[data_start:data_start + cap_len]

    return data, block_information
