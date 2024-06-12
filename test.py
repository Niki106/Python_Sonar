import json

with open('tmp.jsonl', 'r') as f:
    data_string = f.read()

packets = []
for data in data_string.split('\n'):
    if data == '': continue
    packets.append(json.loads(data))

with open('packets2.json', 'w') as f:
    json.dump(packets, f, indent=4)