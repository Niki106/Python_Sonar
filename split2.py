input_file = 'need.working.sl2'
output_file = 'output/split2.sl2'

with open(input_file, 'rb+') as in_file, open(output_file, 'wb') as out_file:
    # Read data before the cut
    in_file.seek(0)
    header = in_file.read(8)

    # Write combined data to output file
    out_file.write(header)

    cnt = 0
    while cnt < 2939:
        in_file.seek(8 + cnt * 4488)
        block = in_file.read(1544)
        out_file.write(block)

        in_file.seek(8 + cnt * 4488 + 1544)
        block = in_file.read(2944)
        out_file.write(block)

        cnt += 1
    
    