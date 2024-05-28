import numpy as np
import pandas as pd
import struct

#Constants
file_head_size_sl2 = 8
frame_head_size_sl2 = 144

def sl2_decode(data):
    position = file_head_size_sl2
    headers = []

    #Cut binary blob
    cnt = 0
    while (position < len(data)):
        head = data[position:(position + frame_head_size_sl2)]
        frame_size = int.from_bytes(head[28:30], "little", signed = False)
        
        # primary = int.from_bytes(head[4:8], "little", signed = False)
        # secondary = int.from_bytes(head[8:12], "little", signed = False)
        # down = int.from_bytes(head[12:16], "little", signed = False)
        # left = int.from_bytes(head[16:20], "little", signed = False)
        # right = int.from_bytes(head[20:24], "little", signed = False)
        # composit = int.from_bytes(head[24:28], "little", signed = False)

        # creation_date_time = int.from_bytes(head[60:64], "little", signed = False)
        # time_offset = int.from_bytes(head[140:144], "little", signed = False)
        lower_limit = struct.unpack('f', head[44:48])[0]
        # channel_type = int.from_bytes(head[32:34], "little", signed = False)
        
        water_depth_feet = struct.unpack('f', head[64:68])[0]
        keels_depth_feet = struct.unpack('f', head[68:72])[0]
        print(lower_limit, water_depth_feet, keels_depth_feet)
        
        # easting = int.from_bytes(head[108:112], "little", signed = False)
        # northing = int.from_bytes(head[112:116], "little", signed = False)

        
        # flags = int.from_bytes(head[132:134], "little", signed = False)   
        # if flags not in (134, 662, 694, 702):
        
        position += frame_size
        cnt += 1
        if cnt == 12000: break
    
if __name__ == '__main__':
    file_name = 'need.working.sl2'
    # file_name = 'output/result.sl2'
    with open(file_name, "rb") as f:
        data = f.read()

    sl2_decode(data)
