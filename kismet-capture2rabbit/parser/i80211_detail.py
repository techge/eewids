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
from elements import parse_element_fields


def i80211_info(i80211, packet, off):

    if (i80211['type'][1] == 'Management'):
        return management(i80211, packet, off)

    if (i80211['type'][1] == 'Control'):
        return control(i80211, packet, off)
        
    return {}


def management(i80211, packet, off):

    elements = parse_element_fields(packet[off:])

    if(i80211['subtype'][1] == 'Beacon' or 
       i80211['subtype'][1] == 'Probe Request' or 
       i80211['subtype'][1] == 'Probe Response'):
    
        elements.update({
                'BSSID': i80211['addr3'],
                })

    return elements


def control(i80211, packet, off):
    return {}

