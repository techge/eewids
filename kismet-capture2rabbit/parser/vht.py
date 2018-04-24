'''
Copyright (c) 2012-2016     Bob Copeland <me@bobcopeland.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

"""
    vht lookups and helpers
    see http://www.radiotap.org/defined-fields/VHT
"""

# vht rate lookups taken from http://mcsindex.com/
vht_rate_table = [
    [6.5, 7.2, 13.5, 15.0, 29.3, 32.5, 58.5, 65.0],
    [13.0, 14.4, 27.0, 30.0, 58.5, 65.0, 117.0, 130.0],
    [19.5, 21.7, 40.5, 45.0, 87.8, 97.5, 175.5, 195.0],
    [26.0, 28.9, 54.0, 60.0, 117.0, 130.0, 234.0, 260.0],
    [39.0, 43.3, 81.0, 90.0, 175.5, 195.0, 351.0, 390.0],
    [52.0, 57.8, 108.0, 120.0, 234.0, 260.0, 468.0, 520.0],
    [58.5, 65.0, 121.5, 135.0, 263.3, 292.5, 526.5, 585.0],
    [65.0, 72.2, 135.0, 150.0, 292.5, 325.0, 585.0, 650.0],
    [78.0, 86.7, 162.0, 180.0, 351.0, 390.0, 702.0, 780.0],
    [None, None, 180.0, 200.0, 390.0, 433.3, 780.0, 866.7],
    [13.0, 14.4, 27.0, 30.0, 58.5, 65.0, 117.0, 130.0],
    [26.0, 28.9, 54.0, 60.0, 117.0, 130.0, 234.0, 260.0],
    [39.0, 43.3, 81.0, 90.0, 175.5, 195.0, 351.0, 390.0],
    [52.0, 57.8, 108.0, 120.0, 234.0, 260.0, 468.0, 520.0],
    [78.0, 86.7, 162.0, 180.0, 351.0, 390.0, 702.0, 780.0],
    [104.0, 115.6, 216.0, 240.0, 468.0, 520.0, 936.0, 1040.0],
    [117.0, 130.3, 243.0, 270.0, 526.5, 585.0, 1053.0, 1170.0],
    [130.0, 144.4, 270.0, 300.0, 585.0, 650.0, 1170.0, 1300.0],
    [156.0, 173.3, 324.0, 360.0, 702.0, 780.0, 1404.0, 1560.0],
    [None, None, 360.0, 400.0, 780.0, 866.7, 1560.0, 1733.3],
    [19.5, 21.7, 40.5, 45.0, 87.8, 97.5, 175.5, 195.0],
    [39.0, 43.3, 81.0, 90.0, 175.5, 195.0, 351.0, 390.0],
    [58.5, 65.0, 121.5, 135.0, 263.3, 292.5, 526.5, 585.0],
    [78.0, 86.7, 162.0, 180.0, 351.0, 390.0, 702.0, 780.0],
    [117.0, 130.0, 243.0, 270.0, 526.5, 585.0, 1053.0, 1170.0],
    [156.0, 173.3, 324.0, 360.0, 702.0, 780.0, 1404.0, 1560.0],
    [175.5, 195.0, 364.5, 405.0, None, None, 1579.5, 1755.0],
    [195.0, 216.7, 405.0, 450.0, 877.5, 975.0, 1755.0, 1950.0],
    [234.0, 260.0, 486.0, 540.0, 1053.0, 1170.0, 2106.0, 2340.0],
    [260.0, 288.9, 540.0, 600.0, 1170.0, 1300.0, None, None],
    [26.0, 28.9, 54.0, 60.0, 117.0, 130.0, 234.0, 260.0],
    [52.0, 57.8, 108.0, 120.0, 234.0, 260.0, 468.0, 520.0],
    [78.0, 86.7, 162.0, 180.0, 351.0, 390.0, 702.0, 780.0],
    [104.0, 115.6, 216.0, 240.0, 468.0, 520.0, 936.0, 1040.0],
    [156.0, 173.3, 324.0, 360.0, 702.0, 780.0, 1404.0, 1560.0],
    [208.0, 231.1, 432.0, 480.0, 936.0, 1040.0, 1872.0, 2080.0],
    [234.0, 260.0, 486.0, 540.0, 1053.0, 1170.0, 2106.0, 2340.0],
    [260.0, 288.9, 540.0, 600.0, 1170.0, 1300.0, 2340.0, 2600.0],
    [312.0, 346.7, 648.0, 720.0, 1404.0, 1560.0, 2808.0, 3120.0],
    [None, None, 720.0, 800.0, 1560.0, 1733.3, 3120.0, 3466.7],
    [None, None, None, None, 146.3, 162.5, 292.5, 325.0],
    [None, None, None, None, 292.5, 325.0, 585.0, 650.0],
    [None, None, None, None, 438.8, 487.5, 877.5, 975.0],
    [None, None, None, None, 585.0, 650.0, 1170.0, 1300.0],
    [None, None, None, None, 877.5, 975.0, 1755.0, 1950.0],
    [None, None, None, None, 1170.0, 1300.0, 2340.0, 2600.0],
    [None, None, None, None, 1316.3, 1462.5, 2632.5, 2925.0],
    [None, None, None, None, 1462.5, 1625.0, 2925.0, 3250.0],
    [None, None, None, None, 1755.0, 1950.0, 3510.0, 3900.0],
    [None, None, None, None, 1950.0, 2166.7, 3900.0, 4333.3],
    [None, None, None, None, 175.5, 195.0, 351.0, 390.0],
    [None, None, None, None, 351.0, 390.0, 702.0, 780.0],
    [None, None, None, None, 526.5, 585.0, 1053.0, 1170.0],
    [None, None, None, None, 702.0, 780.0, 1404.0, 1560.0],
    [None, None, None, None, 1053.0, 1170.0, 2106.0, 2340.0],
    [None, None, None, None, 1404.0, 1560.0, 2808.0, 3120.0],
    [None, None, None, None, 1579.5, 1755.0, 3159.0, 3510.0],
    [None, None, None, None, 1755.0, 1950.0, 3510.0, 3900.0],
    [None, None, None, None, 2106.0, 2340.0, 4212.0, 4680.0],
    [None, None, None, None, None, None, 4680.0, 5200.0],
    [None, None, None, None, 204.8, 227.5, 409.5, 455.0],
    [None, None, None, None, 409.5, 455.0, 819.0, 910.0],
    [None, None, None, None, 614.3, 682.5, 1228.5, 1365.0],
    [None, None, None, None, 819.0, 910.0, 1638.0, 1820.0],
    [None, None, None, None, 1228.5, 1365.0, 2457.0, 2730.0],
    [None, None, None, None, 1638.0, 1820.0, 3276.0, 3640.0],
    [None, None, None, None, None, None, 3685.5, 4095.0],
    [None, None, None, None, 2047.5, 2275.0, 4095.0, 4550.0],
    [None, None, None, None, 2457.0, 2730.0, 4914.0, 5460.0],
    [None, None, None, None, 2730.0, 3033.3, 5460.0, 6066.7],
    [None, None, None, None, 234.0, 260.0, 468.0, 520.0],
    [None, None, None, None, 468.0, 520.0, 936.0, 1040.0],
    [None, None, None, None, 702.0, 780.0, 1404.0, 1560.0],
    [None, None, None, None, 936.0, 1040.0, 1872.0, 2080.0],
    [None, None, None, None, 1404.0, 1560.0, 2808.0, 3120.0],
    [None, None, None, None, 1872.0, 2080.0, 3744.0, 4160.0],
    [None, None, None, None, 2106.0, 2340.0, 4212.0, 4680.0],
    [None, None, None, None, 2340.0, 2600.0, 4680.0, 5200.0],
    [None, None, None, None, 2808.0, 3120.0, 5616.0, 6240.0],
    [None, None, None, None, 3120.0, 3466.7, 6240.0, 6933.3]]

vht_bandwidth_lut = [
    (20, "", None),
    (40, "", None),
    (40, "20L", 0),
    (40, "20U", 1),
    (80, "", None),
    (80, "40L", 0),
    (80, "40U", 1),
    (80, "20LL", 0),
    (80, "20LU", 1),
    (80, "20UL", 2),
    (80, "20UU", 3),
    (160, "", None),
    (160, "80L", 0),
    (160, "80U", 1),
    (160, "40LL", 0),
    (160, "40LU", 1),
    (160, "40UL", 2),
    (160, "40UU", 3),
    (160, "20LLL", 0),
    (160, "20LLU", 1),
    (160, "20LUL", 2),
    (160, "20LUU", 3),
    (160, "20ULL", 4),
    (160, "20ULU", 5),
    (160, "20UUL", 6),
    (160, "20UUU", 7),
]

def vht_rate(vht_mcs_index, nss, gi, bandwidthMHz):
    """vht_mcs_index is 0-9
            gi: 0=long 1=short"""

    def calculate_column_index(gi, bandwidthMHz):
        """ gi: 0=long 1=short"""
        column_offset_by_bwMHz = {20: 0, 40: 2, 80: 4, 160: 6}
        return column_offset_by_bwMHz[bandwidthMHz] + gi

    def calculate_row_index(vht_index, nss):
        return vht_index + (nss - 1) * 10

    col = calculate_column_index(gi, bandwidthMHz)
    row = calculate_row_index(vht_mcs_index, nss)
    return vht_rate_table[row][col]


def vht_rate_description(vht_mcs_index, nss, gi, bandwidthMHz):
    mcs_by_vht_index \
        = {
        0: ("BPSK", "1/2"),
        1: ("QPSK", "1/2"),
        2: ("QPSK", "3/2"),
        3: ("16QAM", "1/2"),
        4: ("16QAM", "3/4"),
        5: ("64QAM", "2/3"),
        6: ("64QAM", "3/4"),
        7: ("64QAM", "5/6"),
        8: ("256QAM", "3/4"),
        9: ("256QAM", "5/6"),
    }
    gi_desc = {0: 800, 1: 400}
    return {'vht_mcs_index': vht_mcs_index,
            'vht_mcs_descr': mcs_by_vht_index[vht_mcs_index],
            'vht_rate_mbps': vht_rate(vht_mcs_index, nss, gi, bandwidthMHz),
            }
