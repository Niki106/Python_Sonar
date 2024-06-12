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

def encode_sl2_frame(packet, index):
    global timestamp
    global prev_frame_size
    global prev_frame_offset

    # Frame data
    data_string = packet['sample_data']
    hex_values = [value.strip() for value in data_string.split(',')]
    byte_array = bytearray([int(value, 16) for value in hex_values])
    sound_data = byte_array

    # Frame
    packet_size = len(sound_data)       # 1400, 2800, 3072, 2880
    frame_size = FRAME_HEADER_SIZE + packet_size
    frame_offset = prev_frame_offset + prev_frame_size

    channel_type = ChannelType.Primary   # ChannelType.DownScan
    
    frame_index = index
    upper_limit = 0 #if (index % 2 == 0) else -5
    lower_limit = 5

    water_depth_feet = int(packet['depth'].strip()) * 0.0328084
    easting = packet['lon'] * EARTH_RADIUS / RAD_CONVERSION
    nothing = EARTH_RADIUS * math.log(math.tan((packet['lat'] / RAD_CONVERSION / 2) + math.pi / 4))
    altitude_ft = packet['alt']

    time_offset = int(packet['timestamp']) - timestamp

    frame_data = {
        "frame_offset": frame_offset,
        "frame_size": frame_size,
        "previous_frame_size": prev_frame_size,
        "channel_type": channel_type,
        "packet_size": packet_size,

        "frame_index": frame_index,
        "upper_limit_feet": upper_limit,
        "lower_limit_feet": lower_limit,

        "_pad48": 0,
        "frequency": 3,
        "_pad51": 0,

        "water_depth_feet": water_depth_feet,
        "keel_depth_feet": 0,

        "_pad2": 0,

        "gps_speed_knots": 0,
        "water_temperature_c": 0,
        "easting": int(easting),
        "northing": int(nothing),
        "water_speed_knots": 0,
        "course_over_ground_radians": 0,
        "altitude_ft": altitude_ft,
        "heading_radians": 0,

        "flags": 134,

        "_pad3": 0,

        "time_offset": time_offset,
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
    i = 0
    timestamp = int(packets[0]['timestamp'])
    for packet in packets:
        frame = encode_sl2_frame(packet, i)
        blocks.append(frame)
        i = i + 1

    # Write data to file
    with open(filename, 'wb') as f:
        # Write file header
        f.write(file_header)

        # Write blocsk
        for block in blocks:
            f.write(block)

if __name__ == '__main__':
    # Open the packets file
    with open("packets2.json", "r") as f:
        data_string = f.read()
    data_string = data_string.replace("'", '"')
    packets = eval(data_string)
    
    # Create output directory
    output_dir = os.getcwd()
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Directory created: {output_dir}")
        except OSError as e:
            print(f"Error creating directory: {e}")

    file_name = os.path.join(output_dir, "result.sl2")
    compose_sl2_file(packets, file_name)