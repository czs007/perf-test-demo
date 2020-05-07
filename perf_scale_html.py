import os
import statistics
import pprint


arctern_path = '/home/czs/scale_report'

PREFIXES = [
        'geomesa', 
        'geospark', 
        'arctern'
        ]


def fetch_log_files(log_dir):
    log_files = []
    files = os.listdir(log_dir)
    for f in files:
        if os.path.splitext(f)[1] == '.txt':
            log_files.append(f)
    return log_dir, log_files


def fetch_func_perf(log_dir, files):
    import re
    res = []
    append_order_arr = []
    for log_file in files:
        tmp_arr = []
        full_path = os.path.join(log_dir, log_file)
        with open(full_path, 'r') as f:
            for line in f:
                line = list(map(lambda x: x.upper(), re.split('[: ]',line.strip())))
                keys = [(k + "_" + log_file[0:-4] + '_time').upper() for k in PREFIXES]
                keys.append((log_file[0:-4]).upper())
                if any(k for k in keys if k in line):
                    tmp_arr.append(float(line[-1]))
        append_order_arr.append(log_file[0:-4])
        res.append(tmp_arr)
    return res, append_order_arr


def extract_all_perf_time(data_path):
    data = {}
    node_nums = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    for num in node_nums:
        _data_path = os.path.join(data_path, num)
        subdirs = [d for d in os.listdir(_data_path) if os.path.isdir(os.path.join(_data_path, d))]
        _data = {}
        for sub in subdirs:
            _data[sub] = extract_perf_time(os.path.join(_data_path, sub))
        data[num] = _data

    return data

def extract_perf_time(data_path):
    res_set, func_order = fetch_func_perf(*fetch_log_files(data_path))
    func_order = [x.lower() for x in func_order if isinstance(x, str)]

    assert len(func_order) == len(res_set)
    result = {}
    for i in range(len(func_order)):
        func_name = func_order[i]
        nums = res_set[i][1:]
        mean = 0
        if nums:
            mean = statistics.mean(nums)
        result[func_name] = mean

    return result

def write_data(data, output_path):

    # "scale": ('REP_NODES', 'REP_SET_NAMES', 'REP_DATASETS', 'REP_FUNC_NAMES'),
    rep_data = {}
    data_keys = list(set(data.keys()))
    data_keys.sort()

    all_set_names = set()
    all_func_names = set()
    for k in data_keys:
        set_names = set(data[k].keys())
        all_set_names |= set_names
        for set_name in set_names:
            all_func_names |= set(data[k][set_name])

    # REP_NODES
    all_func_names = list(all_func_names)
    all_func_names.sort()
    all_set_names = list(all_set_names)
    all_set_names.sort()

    data_sets = []
    for func_name in all_func_names:
        set_data = []
        for set_name in all_set_names:
            node_data = []
            for node_num in data_keys:
                value = data.get(node_num, {}).get(set_name, {}).get(func_name, 0)
                node_data.append(str(value))
            set_data.append(','.join(node_data))
        data_sets.append(':'.join(set_data))

    rep_data = {
        'REP_NODES': data_keys,
        'REP_SET_NAMES' : all_set_names,
        'REP_DATASETS' : data_sets,
        'REP_FUNC_NAMES' : all_func_names,
    }

    with open (output_path, "w") as f:
        f.write(str(rep_data))

def print_help():
    print('python perf_analyze.py  -d <data_path> -o <output_path>')

if __name__ == "__main__":

    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "-d:-o:-h",['data_path','output_path','help'])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    data_path = ""
    output_path = "./hehe"

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-d", "--data_path"):
            data_path = arg
        elif opt in ("-o", "--output_path"):
            output_path = arg

    data_path = arctern_path
    if "" in (data_path, output_path):
        print_help()
        sys.exit()

    if not os.path.exists(data_path):
        print_help()
        sys.exit()

    data = extract_all_perf_time(data_path)
    write_data(data, output_path)
