import math
from schemas_navico import sl_file_header, sl2_frame, ChannelType
import os

def lon2x(lon):
    # Convert from degrees to radians
    lon_radians = math.radians(lon)

    # Apply the inverse formula from x2lon
    x = lon_radians * 6356752.3142 * (1 / math.pi)

    return x

def lat2y(lat):
    # Convert latitude to radians
    rad_lat = math.radians(lat)

    # WGS-84 equatorial radius
    a = 6378137.0  # meters

    # WGS-84 eccentricity squared
    e2 = 0.0066934213 

    # Calculate y (latitude in meters)
    y = a * math.log(math.tan(math.pi/4 + rad_lat / 2) * math.sqrt((1 - e2) / (1 + e2 * math.sin(rad_lat)**2)))
    return y

def encode_sl2(packet, filename):
    # File header
    version = 2             # 02 = sl2 format
    hardware_version = 0    # 00 = ex HDS 7, 01 = ex. Elite 4 CHIP
    blocksize = 3200        # 1970 = Downscan #b207, 3200 = Sidescan #800c
    padding = 0

    file_header_data = {
        "version": version,
        "hardware_version": hardware_version,
        "block_size": blocksize,
        "p_": padding
    }
    file_header = sl_file_header.build(file_header_data)

    # Frame data
    data_string = packet['sample_data']
    hex_values = [value.strip() for value in data_string.split(',')]
    byte_array = bytearray([int(value, 16) for value in hex_values])
    sounded_data = byte_array

    # Frame
    frame_offset = 8
    frame_size = len(sounded_data) + 144
    channel_type = ChannelType.SidescanComposite
    packet_size = len(sounded_data)
    water_depth_feet = int(packet['depth'].strip()) # Depth
    x = int(lon2x(packet['lon']))                        # x from longitude
    y = int(lat2y(packet['lat']))                        # y from latitude

    frame_data = {
        "frame_offset": frame_offset,
        
        "frame_size": frame_size,
        "previous_frame_size": 0,
        "channel_type": channel_type,
        "packet_size": packet_size,

        "frame_index": 0,
        "upper_limit_feet": 0,
        "lower_limit_feet": 0,

        "_pad48": 0,
        "frequency": 0,
        "_pad51": 0,

        "water_depth_feet": water_depth_feet,
        "keel_depth_feet": 0,

        "_pad2": 0,

        "gps_speed_knots": 0,
        "water_temperature_c": 0,
        "easting": x,
        "northing": y,
        "water_speed_knots": 0,
        "course_over_ground_radians": 0,
        "altitude_ft": 0,
        "heading_radians": 0,

        "flags": 0,

        "_pad3": 0,

        "time_offset": 0,
        "sounded_data": sounded_data,
    }
    frame = sl2_frame.build(frame_data)

    # Write data to file
    with open(filename, 'wb') as f:
        # Write file header
        f.write(file_header)

        # Write frame
        f.write(frame)

if __name__ == '__main__':
    # Open the packets file
    with open("packets.py", "r") as f:
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

    # Write the sl2 file for each packet
    i = 1
    for packet in packets:
        file_name = os.path.join(output_dir, str(i).zfill(2) + ".sl2")
        i = i + 1
        if not 'lon' in packet: continue
        encode_sl2(packet, file_name)
        # break