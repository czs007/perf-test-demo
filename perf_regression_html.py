import os
import statistics

ROWS = 10**6

LOG_DIRS = {
    'geospark': '/home/czs/performance/geospark_log/',
    'geomesa': '/home/czs/performance/geomesa_log/',
    'arctern': '/home/czs/performance/arctern_log/',
}

template_html = ''
html_path = ''

PREFIXES = [
        'geomesa', 
        'geospark', 
        'arctern'
        ]

COLORS = [
        (0.2, 0.4, 0.6, 0.6),
        (0.2, 0.4, 0.5, 0.5),
        (0.2, 0.4, 0.4, 0.4)
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
        with open(log_dir + log_file, 'r') as f:
            for line in f:
                line = list(map(lambda x: x.upper(), re.split('[: ]',line.strip())))
                keys = [(k + "_" + log_file[0:-4] + '_time').upper() for k in PREFIXES]
                keys.append((log_file[0:-4]).upper())
                if any(k for k in keys if k in line):
                    tmp_arr.append(float(line[-1]))
        append_order_arr.append(log_file[0:-4])
        res.append(tmp_arr)
    return res, append_order_arr


def extract_perf_time(log_dir):
    res_set, func_order = fetch_func_perf(*fetch_log_files(log_dir))
    func_order = [x.lower() for x in func_order if isinstance(x, str)]

    assert len(func_order) == len(res_set)
    result = {}
    for i in range(len(func_order)):
        func_name = func_order[i]
        nums = res_set[i][1:]
        mean = statistics.mean(nums)
        result[func_name] = mean

    return result

def extract_common_funcs_and_times(means_list):
    keys_list = [set(d) for d in means_list]
    keys = set.intersection(*keys_list)
    result = {}
    cnt = len(means_list)
    for k in keys:
        pair = []
        for i in range(cnt):
            data = means_list[i]
            pair.append(data[k])
        result[k] = pair
    return result

def read_and_replace(data):
    REP_DATA_NAMES = PREFIXES
    function_names = list(data.keys())
    data_sets = []

    for i, data_name in enumerate(REP_DATA_NAMES):
        _data = []
        for name in function_names:
            _data.append(str(data[name][i]))
        data_sets.append(",".join(_data))

    from math import log, ceil
    row_str = '10_' + str(ceil(log(ROWS, 10)))

    rep_data = {
            'ROWS': row_str,
            'REP_DATA_NAMES' : PREFIXES,
            'REP_DATASETS' : data_sets,
            'REP_FUNC_NAMES' : function_names,
        }

    with open (template_path, "r") as f:
        lines = f.readlines()
        all_string = "".join(lines)
        for k, v in rep_data.items():
            all_string = all_string.replace(k, str(v))

    if all_string:
        with open (html_path, "w") as f:
            f.write(all_string)

if __name__ == "__main__":

    import sys
    import getopt


    try:
        opts, args = getopt.getopt(sys.argv[1:], "-a:-b:-c:-r:-p:-t:-h",['geospark_dir','geomesa_dir','arctern_dir','rows','template_path','html_path','help'])
    except getopt.GetoptError:
        print('python perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -r <rows> -p <template_path> -t <html_path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -r <rows> -p <template_path> -t <html_path>')
            sys.exit()
        elif opt in ("-a", "--geospark_dir"):
            LOG_DIRS['geospark'] = arg
        elif opt in ("-b", "--geomesa_dir"):
            LOG_DIRS['geomesa'] = arg
        elif opt in ("-c", "--arctern_dir"):
            LOG_DIRS['arctern'] = arg
        elif opt in ("-r", "--rows"):
            ROWS = int(arg)
        elif opt in ("-p", "--template_path"):
            template_path = arg
        elif opt in ("-t", "--html_path"):
            html_path = arg

    mean_list = [] 

    from math import log, ceil
    sub_dir = '10_' + str(ceil(log(ROWS, 10))) + '/'
    for prefix in PREFIXES:
        log_dir = LOG_DIRS[prefix]
        log_dir += sub_dir
        mean_list.append(extract_perf_time(log_dir))

    res = extract_common_funcs_and_times(mean_list)
    read_and_replace(res)
