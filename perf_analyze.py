
import os

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import statistics

ROWS = 10**6

LOG_DIRS = {
    'geospark': '/home/czs/performance/geospark_log/',
    'geomesa': '/home/czs/performance/geomesa_log/',
    'arctern': '/home/czs/performance/arctern_log/',
}

plot_dir = 'perf/pic/'
fig_title = 'performance analysis fig'
png_name = 'perf'

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


def plot_histogram(plot_data, file_name,fig_name):

    func_list = list(plot_data.keys())
    histogram_file = plot_dir + '/'+file_name + '.png'
    fig_title = fig_name

    x = list(range(len(func_list)))
    total_width, n = 0.9, 3
    width = total_width / n
    plt.figure(figsize=(36, 4))  # picture size
    plt.title(fig_title)
    plt.xlabel("Functions")  # X label
    plt.ylabel("Cost /ms")  # Y label

    for i, prefix in enumerate(PREFIXES):
        res_ret = [plot_data[k][i] for k in func_list]
        plt.bar(x, res_ret, width=width, label=prefix, color=COLORS[i])
        for j in range(len(x)):
            x[j] = x[j] + width

    middle_x = list(range(len(func_list)))
    offset = (len(PREFIXES) - 1) * 0.5 * width
    middle_x = [x + offset for x in middle_x]

    plt.legend()
    plt.xticks(middle_x, func_list)
    plt.savefig(histogram_file)
    plt.close('all')


if __name__ == "__main__":

    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-a:-b:-c:-r:-p:-t:-n:-h",['geospark_dir','geomesa_dir','arctern_dir','rows','plot_dir','fig_title','png_name','help'])
    except getopt.GetoptError:
        print('python perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -r <rows> -p <plot_dir> -t <fig_title> -n <png_name>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -r <rows> -p <plot_dir> -t <fig_title> -n <png_name>')
            sys.exit()
        elif opt in ("-a", "--geospark_dir"):
            LOG_DIRS['geospark'] = arg
        elif opt in ("-b", "--geomesa_dir"):
            LOG_DIRS['geomesa'] = arg
        elif opt in ("-c", "--arctern_dir"):
            LOG_DIRS['arctern'] = arg
        elif opt in ("-r", "--rows"):
            ROWS = int(arg)
        elif opt in ("-p", "--plot_dir"):
            plot_dir = arg
        elif opt in ("-t", "--fig_title"):
            fig_title = arg
        elif opt in ("-n", "--png_name"):
            png_name = arg

    mean_list = [] 

    from math import log, ceil
    sub_dir = '10_' + str(ceil(log(ROWS, 10))) + '/'
    for prefix in PREFIXES:
        log_dir = LOG_DIRS[prefix]
        log_dir += sub_dir
        mean_list.append(extract_perf_time(log_dir))

    res = extract_common_funcs_and_times(mean_list)
    plot_histogram(res, "a", "hehe")
