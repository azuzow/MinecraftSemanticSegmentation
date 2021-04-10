def read_labels(file):
    f = open(file, "r")
    label_dict = {}
    index_dict = {}
    while True:
        line = f.readline()   
        if not line:
            break
        line_parsed = line.strip().split(':')
        print(line_parsed)
        rgb = tuple([int(c) for c in line_parsed[-2].split(',')])
        label_dict[rgb] = line_parsed[-1]

        index_dict[rgb] = line_parsed[0]
   
    return label_dict, index_dict
