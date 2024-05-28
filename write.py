import math
from schemas_navico import sl_file_header, sl2_frame, ChannelType
import os

EARTH_RADIUS = 6356752.3142
RAD_CONVERSION = 180 / math.pi

timestamp = 0
prev_frame_size = 0

def encode_sl2_frame(packet, index):
    global timestamp
    global prev_frame_size

    # Frame data
    data_string = packet['sample_data']
    hex_values = [value.strip() for value in data_string.split(',')]
    byte_array = bytearray([int(value, 16) for value in hex_values])
    sounded_data = byte_array

    # Frame
    frame_size = len(sounded_data) + 144
    frame_offset = 8 + index * frame_size
    channel_type = ChannelType.SidescanComposite
    packet_size = len(sounded_data)
    
    frame_index = index
    upper_limit = 0
    lower_limit = 5.0

    water_depth_feet = 3.5 # int(packet['depth'].strip()) # Depth
    easting = packet['lon'] * EARTH_RADIUS / RAD_CONVERSION
    nothing = EARTH_RADIUS * math.log(math.tan((packet['lat'] / RAD_CONVERSION / 2) + math.pi / 4))

    altitude_ft = 0
    time_offset = int(packet['timestamp']) - timestamp

    frame_data = {
        "frame_offset": frame_offset,
        "last_frame_offset_down_scan": frame_offset,
        
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
        "sounded_data": sounded_data,
    }

    frame = sl2_frame.build(frame_data)

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
        if not 'lon' in packet: continue
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
    with open("packets.json", "r") as f:
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