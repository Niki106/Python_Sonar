import numpy as np
import pandas as pd
import struct
import json

#Constants
file_head_size_sl2 = 8
frame_head_size_sl2 = 144

def sl2_decode(data):
    position = file_head_size_sl2

    packets = []

    #Cut binary blob
    cnt = 0
    while (position < len(data)):
        head = data[position:(position + frame_head_size_sl2)]
        
        frame_offset = int.from_bytes(head[0:4], "little", signed = False)
        frame_size = int.from_bytes(head[28:30], "little", signed = False)
        prev_frame_size = int.from_bytes(head[30:32], "little", signed = False)
        channel_type = int.from_bytes(head[32:34], "little", signed = False)
        packet_size = int.from_bytes(head[34:36], "little", signed = False)
        frame_index = int.from_bytes(head[36:40], "little", signed = False)
        upper_limit = struct.unpack('f', head[40:44])[0]
        lower_limit = struct.unpack('f', head[44:48])[0]
        frequency = int.from_bytes(head[53:54], "little", signed = False)
        creation_date_time = int.from_bytes(head[60:64], "little", signed = False)
        water_depth_feet = struct.unpack('f', head[64:68])[0]
        keels_depth_feet = struct.unpack('f', head[68:72])[0]
        
        gps_speed_knots = struct.unpack('f', head[100:104])[0]
        water_temperature_c = struct.unpack('f', head[104:108])[0]

        easting = int.from_bytes(head[108:112], "little", signed = True)
        northing = int.from_bytes(head[112:116], "little", signed = True)
        
        water_speed_knots = struct.unpack('f', head[116:120])[0]
        course_over_ground_radians = struct.unpack('f', head[120:124])[0]

        flags = int.from_bytes(head[132:134], "little", signed = False)

        time_offset = int.from_bytes(head[140:144], "little", signed = False)

        sound = data[(position + frame_head_size_sl2):(position + frame_size)]
        sound_array = [f"{b:02x}" for b in sound]
        sound_str = ','.join(sound_array)
     
        packet = {
            "frame_offset": frame_offset,
            "frame_size": frame_size,
            "prev_frame_size": prev_frame_size,
            "channel_type": channel_type,
            "packet_size": packet_size,
            "frame_index": frame_index,
            "upper_limit": upper_limit,
            "lower_limit": lower_limit,
            "frequency": frequency,
            "creation_date_time": creation_date_time,
            "water_depth_feet": water_depth_feet,
            "keels_depth_feet": keels_depth_feet,
            "gps_speed_knots": gps_speed_knots,
            "water_temperature_c": water_temperature_c,
            "easting": easting,
            "northing": northing,
            "water_speed_knots": water_speed_knots,
            "course_over_ground_radians": course_over_ground_radians,
            "flags": flags,
            "time_offset": time_offset,
            "sound_data": sound_str
        }

        packets.append(packet)

        # heading = struct.unpack('f', head[128:132])[0]
        
        # flags = int.from_bytes(head[132:134], "little", signed = False)   
        # if flags not in (134, 662, 694, 702):
        
        position += frame_size

        cnt += 1
        # if cnt == 12000: break
    
    with open('output/split2.json', 'w') as output:
        json.dump(packets, output, indent=4)
    
if __name__ == '__main__':
    file_name = 'output/split2.sl2'
    # file_name = 'output/result.sl2'
    with open(file_name, "rb") as f:
        data = f.read()

    sl2_decode(data)
