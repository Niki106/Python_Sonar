import math
from schemas_navico import sl_file_header, sl2_frame, ChannelType
import os

EARTH_RADIUS = 6356752.3142
RAD_CONVERSION = 180 / math.pi
FILE_HEADER_SIZE = 8
FRAME_HEADER_SIZE = 144

timestamp = 0
prev_frame_size = 0
prev_frame_offset = FILE_HEADER_SIZE

def encode_sl2_block(packet):
    global prev_frame_size
    global prev_frame_offset

    # Frame data
    data_string = packet['sound_data']
    hex_values = [value.strip() for value in data_string.split(',')]
    byte_array = bytearray([int(value, 16) for value in hex_values])
    sound_data = byte_array 

    packet_size = len(sound_data)       # 1400, 2800, 3072, 2880
    frame_size = FRAME_HEADER_SIZE + packet_size
    frame_offset = prev_frame_offset + prev_frame_size
    
    # Frame
    frame_data = {
        "frame_offset": frame_offset,                           # packet['frame_offset'],
        "frame_size": frame_size,                               # packet['frame_size'],
        "previous_frame_size": prev_frame_size,                 # packet['prev_frame_size'],
        "channel_type": packet['channel_type'],
        "packet_size": packet_size,                             # packet['packet_size'],

        "frame_index": packet['frame_index'],
        "upper_limit_feet": 0, #packet['upper_limit'],
        "lower_limit_feet": 5, #packet['lower_limit'],

        "_pad48": 0,
        "frequency": 3, #packet['frequency'],
        "_pad51": 0,

        "water_depth_feet": 0, #packet['water_depth_feet'],
        "keel_depth_feet": 0, #packet['keels_depth_feet'],

        "_pad2": 0,

        "gps_speed_knots": 0, #packet['gps_speed_knots'],
        "water_temperature_c": 0, #packet['water_temperature_c'],
        "easting": packet['easting'],
        "northing": packet['northing'],
        "water_speed_knots": 0, #packet['water_speed_knots'],
        "course_over_ground_radians": 0, #packet['course_over_ground_radians'], 
        "altitude_ft": 0,
        "heading_radians": 0,

        "flags": packet['flags'],

        "_pad3": 0,

        "time_offset": packet['time_offset'],
        "sounded_data": sound_data,
    }

    frame = sl2_frame.build(frame_data)
    
    # Store for next calculation
    prev_frame_offset = frame_offset
    prev_frame_size = frame_size

    return frame

def compose_sl2_file(packets, filename):
    global timestamp

    # File header
    version = 2             # 02 = sl2 format
    hardware_version = 1    # 00 = ex HDS 7, 01 = ex. Elite 4 CHIP
    blocksize = 3200        # 1970 = Downscan #b207, 3200 = Sidescan #800c
    padding = 0

    file_header_data = {
        "version": version,
        "hardware_version": hardware_version,
        "block_size": blocksize,
        "p_": padding
    }

    file_header = sl_file_header.build(file_header_data)

    # encode frames
    blocks = []
    for packet in packets:
        block = encode_sl2_block(packet)
        blocks.append(block)

    # Write data to file
    with open(filename, 'wb') as f:
        # Write file header
        f.write(file_header)

        # Write blocsk
        for block in blocks:
            f.write(block)

if __name__ == '__main__':
    # Open the packets file
    with open("output/split2.json", "r") as f:
        data_string = f.read()
    data_string = data_string.replace("'", '"')
    packets = eval(data_string)
    
    compose_sl2_file(packets, "output/result2.sl2")