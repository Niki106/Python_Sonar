import json

with open("packets.py", "r") as f:
    data_string = f.read()
data_string = data_string.replace("'", '"')
packets = eval(data_string)

with open("packets2k.py", "r") as f:
    data_string = f.read()
data_string = data_string.replace("'", '"')
packets2 = eval(data_string)

for packet in packets2:
    packet['lat'] = packets[2]['lat']
    packet['lon'] = packets[2]['lon']
    packet['alt'] = packets[2]['alt']

filename = 'packets2k_new'
with open(filename, 'w') as f:
    json.dump(packets2, f, indent=4)