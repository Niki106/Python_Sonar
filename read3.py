from pathlib import Path
import construct as c
from schemas_navico import sl_file_header, sl2_frame
import json

if __name__ == '__main__':
    file_bytes = Path('./need.working.sl2').read_bytes()

    header = sl_file_header.parse(file_bytes[:8])
    blocks = []

    c = 0
    i = 8
    while i < len(file_bytes):
        try:
            frame = sl2_frame.parse(file_bytes[i:])
            assert frame.frame_offset == i
            i += frame.frame_size
            blocks.append(frame)
            # if c == 5: break
            c += 1

            # v in frame.flags.items() if v and k!='_flagsenum')))
        except c.ConstructError as e:
            print(f'failed to parse block at {i} for reason: {e}')

    pass

    new_blocks = []
    for block in blocks:
        dic = dict(block)
        del dic["sounded_data"]
        del dic["_io"]
        new_blocks.append(dic)

    filename = 'joe.json'
    with open(filename, 'w') as f:
        json.dump(new_blocks, f, indent=4)
