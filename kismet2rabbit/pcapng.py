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


"""
Returns the size (in Bytes) of next block in stream as saved in Block Total Length field
Value is 0 if no complete block is included in stream yet
"""
def block_total_length(stream):

    if (len(stream) >= 8):
        return int.from_bytes(stream[4:8], byteorder='little')

    return 0


"""
Extracts block type and extract information found in block
"""
def block_processing(stream):
    
    if (stream[0:4] == b'\n\r\r\n'):
        return block_section_header(stream)

    if (stream[0:4] == b'\x01\x00\x00\x00'):
        return block_interface_description(stream)
    
    if (stream[0:4] == b'\x06\x00\x00\x00'):
        return block_enhanced(stream)

    else:
        print("\r\nUnknown Block Block Type. Skipping.")
        return None, None


"""
Processing Section Header Block
"""
def block_section_header(stream):

    block_information = {
        'block_type':   (0, 'Section Header Block'),
        'length':       stream[4:8].hex(),
        'byteorder':    stream[8:12].hex(),
        'major_ver':    stream[12:14].hex(),
        'minor_ver':    stream[14:16].hex(),
    }

    enddata = int.from_bytes(stream[4:8], byteorder='little') - 4

    if (stream[4:8] != stream[enddata:]):
        print("Warning: Section Header Block broken\r\n",
              "first and second total length field do not match")

    return None, block_information


"""
Processing Interface Description Block
"""
def block_interface_description(stream):

    block_information = {
        'block_type':   (1, 'Interface Description Block'),
        'length':       stream[4:8].hex(),
        'linktype':     stream[8:10].hex(),
        #'reserved':     stream[10:12].hex(),
        'snaplen':      stream[12:16].hex(),
    }

    enddata = int.from_bytes(stream[4:8], byteorder='little') - 4

    if (stream[4:8] != stream[enddata:]):
        print("Warning: Interface Description Block broken\r\n",
              "first and second total length field do not match")

    optionbyte = 16

    # processing option fields
    # there are a lot more option fields, but they does not seem to be used by Kismet
    # -> ignoring for now
    while (optionbyte < enddata):
        
        length = int.from_bytes(stream[optionbyte+2:optionbyte+4], byteorder='little')
        
        # if_name option field
        if (stream[optionbyte:optionbyte+2] == b'\x02\x00'):
            block_information.update({
                'if_name': stream[optionbyte + 4:optionbyte +4 + length],
            })

        # end of option fields
        if (stream[optionbyte:optionbyte+2] == b'\x00\x00'):
            break

        padding = (4 - length%4)%4 
        optionbyte = optionbyte + 4 + length + padding

    return None, block_information


"""
Processing Enhanced Packet Block
"""
def block_enhanced(stream):
    
    block_information = {
        'block_type':   (6, 'Enhanced Packet Block'),
        'length':       stream[4:8].hex(),
        'interface_ID': stream[8:12].hex(),
        'time_high':    stream[12:16].hex(),
        'time_low':     stream[16:20].hex(),
    }

    enddata = int.from_bytes(stream[4:8], byteorder='little') - 4

    if (stream[4:8] != stream[enddata:]):
        print("Warning: Enhanced Packet Block broken\r\n",
              "first and second total length field do not match")

    if (stream[20:24] != stream[24:28]):
        print("Warning: Packet was not captured completey!")

    off = stream[28:enddata]

    return off, block_information
