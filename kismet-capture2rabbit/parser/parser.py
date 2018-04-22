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

from i80211_detail import i80211_info
from radiotap import radiotap_parse, ieee80211_parse


def packet_parse(packet):

    off, radiotap = radiotap_parse(packet)
    off, i80211 = ieee80211_parse(packet, off)
    i80211_detail = i80211_info(i80211, packet, off)
    parsed = radiotap
    parsed.update(i80211)
    parsed.update(i80211_detail)

    return parsed
