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


from i80211_detail import i80211_info
from radiotap import radiotap_parse, ieee80211_parse


def packet_parse(packet):

    off, radiotap = radiotap_parse(packet)
    off, i80211 = ieee80211_parse(packet, off)
    # TODO fix ahead, better clean it!
    # note: this is done to remove the frame check sequence from packet_data
    i80211_detail = i80211_info(i80211, packet[0:len(packet)-4], off)
    parsed = radiotap
    parsed.update(i80211)
    parsed.update(i80211_detail)

    return parsed
