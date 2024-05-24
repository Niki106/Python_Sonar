from pathlib import Path
import construct as c
import json

from schemas_navico import sl_file_header, sl2_frame
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file_bytes = Path('./output/02.sl2').read_bytes()

    header = sl_file_header.parse(file_bytes[:8])
    blocks = []

    i = 8
    while i < len(file_bytes):
        try:
            frame = sl2_frame.parse(file_bytes[i:])
            assert frame.frame_offset == i
            i += frame.frame_size
            blocks.append(frame)
            print(frame.easting, frame.northing)
            if str(frame.channel_type) == 'SidescanComposite':
                plt.hist(frame.sounded_data, 100)
                plt.show()
            # v in frame.flags.items() if v and k!='_flagsenum')))
        except c.ConstructError as e:
            print(f'failed to parse block at {i} for reason: {e}')

    pass