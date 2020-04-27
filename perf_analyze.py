import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def fetch_log_files(dir):
    log_files = []
    files = os.listdir(dir)
    for f in files:
        if os.path.splitext(f)[1] == '.txt':
            log_files.append(f)
    return dir, log_files


def fetch_func_perf(log_files):
    # declare var res_arrs based on func_name
    import re
    res = []
    append_order_arr = []
    for func_name in list(map(lambda x: x[0:-4], log_files[1])):
        exec('res_{}=[]'.format(func_name))
    for log_file in log_files[1]:
        tmp_arr = []
        with open(log_files[0] + log_file, 'r') as f:
            for line in f:
                #line = list(map(lambda x: x.upper(), line.split(':')))
                line = list(map(lambda x: x.upper(), re.split('[: ]',line)))
                parser_key1 = ('geospark_' + log_file[0:-4] + '_time').upper()
                parser_key2 = ('geomesa_' + log_file[0:-4] + '_time').upper()
                parser_key3 = ('arctern_' + log_file[0:-4] + '_time').upper()
                parser_key4 = (log_file[0:-4]).upper()
                if parser_key1 in line or parser_key2 in line or parser_key3 in line or parser_key4 in line:
                    tmp_arr.append(float(line[-1]))
        append_order_arr.append(log_file[0:-4])
        res.append(tmp_arr)
    return res, append_order_arr


def perf_stability_alarm(func_name, res_func_arr):
    warning_str = ' [Warning] : The performance of ' + str(func_name) + ' fluctuates greatly!'
    # warning based on standard deviation
    std_deviation = numpy.std(res_func_arr, ddof=1)
    if std_deviation > std_threshold:
        return 1
    return 0


# This function plot line-chart for per funcs to describe the volatility of function running multiple times
# Usage : plot_line_chart('ST_Point',res_ST_Point) --> ST_Point.png
def plot_line_chart(func_name, res_func_arr):
    perf_picture = plot_dir + str(func_name) + '_perf.png'
    perf_fig_title = str(func_name) + ' Performance Fig'

    # plot
    index1 = list(range(1, len(res_func_arr)))
    plt.figure(figsize=(16, 4))  # picture size
    plt.plot(index1, res_func_arr[1:], marker='o', label="$10k$", linestyle='-', color="blue", linewidth=1)
    for a, b in zip(index1, res_func_arr[1:]):
        plt.text(a, b, round(b, 3), ha='center', va='bottom', fontsize=12)
    plt.xlabel("Version ")  # X label
    plt.ylabel("Cost /ms")  # Y label
    plt.title(perf_fig_title)
    x0 = len(res_func_arr)
    y0 = res_func_arr[x0 - 1]
    std_deviation = numpy.std(res_func_arr, ddof=1)
    mean = numpy.mean(res_func_arr)
    # plt.annotate('std :%s\n'%std_deviation+'mean :%s'%mean, xy=(x0, y0), xytext=(+30, -30), textcoords='offset points', fontsize=12,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    plt.text(x0, y0, 'std :%s\n' % round(std_deviation, 5) + 'mean :%s' % round(mean, 5),
             bbox=dict(facecolor='g', edgecolor='gray', alpha=0.1), fontsize=14)
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(10)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlim(0, len(res_func_arr) + 2)
    plt.ylim(min(res_func_arr) - 20, max(res_func_arr) + 10)
    plt.legend()
    # plt.show()
    plt.savefig(perf_picture)
    plt.close('all')
    # print('plot %s performance analysis picture success.'%func_name)

def plot_histogram2(func_order_list,res_set,file_name,fig_name):
    histogram_file = plot_dir + file_name + '.png'
    fig_title = fig_name

    geospark_res = res_set[0]
    geomesa_res = res_set[1]
    x = list(range(len(geospark_res)))
    total_width, n = 0.8, 2
    width = total_width / n
    plt.figure(figsize=(36, 4))  # picture size
    plt.title(fig_title)
    plt.xlabel("Functions")  # X label
    plt.ylabel("Cost /ms")  # Y label
    plt.bar(x, geospark_res, width=width, label='geospark', color=(0.2, 0.4, 0.6, 0.6))
    for i in range(len(x)):
        x[i] = x[i] + width

    plt.bar(x, geomesa_res, width=width, label='geomesa',color=(0.2, 0.4, 0.5, 0.5))
    plt.legend()
    plt.xticks(list(map(lambda x:x-width/2,x)), func_order_list)
    # plt.show()
    plt.savefig(histogram_file)
    plt.close('all')

def plot_histogram3(func_order_list,res_set,file_name,fig_name):
    histogram_file = plot_dir + '/'+file_name + '.png'
    fig_title = fig_name

    geospark_res = res_set[0]
    geomesa_res = res_set[1]
    arctern_res = res_set[2]
    assert len(geospark_res) == len(geomesa_res)
    assert len(geospark_res) == len(arctern_res)

    x = list(range(len(geospark_res)))
    total_width, n = 0.9, 3
    width = total_width / n
    plt.figure(figsize=(36, 4))  # picture size
    plt.title(fig_title)
    plt.xlabel("Functions")  # X label
    plt.ylabel("Cost /ms")  # Y label
    plt.bar(x, geospark_res, width=width, label='geospark', color=(0.2, 0.4, 0.6, 0.6))
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, geomesa_res, width=width, label='geomesa',color=(0.2, 0.4, 0.5, 0.5))
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, arctern_res, width=width, label='arctern', color=(0.2, 0.4, 0.4, 0.4))

    plt.legend()
    plt.xticks(list(map(lambda x:x-width,x)), func_order_list)
    # plt.show()
    plt.savefig(histogram_file)
    plt.close('all')

def figure_intersection2(res_set, geospark_funcs, geomesa_funcs):
    intersection_funcs = [i for i in geospark_funcs if i in geomesa_funcs]
    geospark_res = res_set[0]
    geomesa_res = res_set[1]
    geospark_remove = []
    geomesa_remove = []

    assert len(geospark_funcs) == len(res_set[0])
    assert len(geomesa_funcs) == len(res_set[1])

    delete_index = []
    for i in range(0, len(geospark_funcs)):
        if geospark_funcs[i] not in intersection_funcs or geospark_res[i] == -1:
            delete_index.append(i)
            geospark_remove.append(geospark_funcs[i])
    for i in delete_index[::-1]:
        del geospark_res[i]

    delete_index = []
    for i in range(0, len(geomesa_funcs)):
        if geomesa_funcs[i] not in intersection_funcs or geomesa_res[i] == -1:
            delete_index.append(i)
            geomesa_remove.append(geomesa_funcs[i])
    for i in delete_index[::-1]:
        del geomesa_res[i]


    return intersection_funcs, [geospark_res, geomesa_res], geospark_remove, geomesa_remove

def figure_intersection3(res_set, geospark_funcs, geomesa_funcs,arctern_funcs):
    intersection_funcs = [i for i in geospark_funcs if i in geomesa_funcs and i in arctern_funcs]
    geospark_res = res_set[0]
    geomesa_res = res_set[1]
    arctern_res = res_set[2]
    geospark_remove = []
    geomesa_remove = []
    arctern_remove = []

    assert len(geospark_funcs) == len(res_set[0])
    assert len(geomesa_funcs) == len(res_set[1])
    assert len(arctern_funcs) == len(res_set[2])

    delete_index = []
    for i in range(0, len(geospark_funcs)):
        if geospark_funcs[i] not in intersection_funcs or geospark_res[i] == -1:
            delete_index.append(i)
            geospark_remove.append(geospark_funcs[i])
    for i in delete_index[::-1]:
        del geospark_res[i]

    delete_index = []
    for i in range(0, len(geomesa_funcs)):
        if geomesa_funcs[i] not in intersection_funcs or geomesa_res[i] == -1:
            delete_index.append(i)
            geomesa_remove.append(geomesa_funcs[i])
    for i in delete_index[::-1]:
        del geomesa_res[i]

    delete_index = []
    for i in range(0, len(arctern_funcs)):
        if arctern_funcs[i] not in intersection_funcs or arctern_res[i] == -1:
            delete_index.append(i)
            arctern_remove.append(arctern_funcs[i])
    for i in delete_index[::-1]:
        del arctern_res[i]

    return intersection_funcs, [geospark_res, geomesa_res,arctern_res], geospark_remove, geomesa_remove, arctern_remove

def re_order(standard_order_arr,index_arr,value_arr):
    for item in standard_order_arr:
        yield dict(zip(index_arr,value_arr))[item]

geospark_log_dir = '/home/czp/performance/geospark_log/10_7/'
geomesa_log_dir = '/home/czp/performance/geomesa_log/10_7/'
arctern_log_dir = '/home/czp/performance/arctern_log/10_7/'
plot_dir = 'perf/pic/'
fig_title = 'performance analysis fig'
png_name = 'perf'

# Performance analysis standard deviation accuracy tolerance
std_threshold = 3.0

if __name__ == "__main__":
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-a:-b:-c:-p:-t:-n:-h",['geospark_dir','geomesa_dir','arctern_dir','plot_dir','fig_title','png_name','help'])
    except getopt.GetoptError:
        print('python perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -p <plot_dir> -t <fig_title> -n <png_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('perf_analyze.py -a <geospark_dir> -b <geomesa_dir> -c <arctern_dir> -p <plot_dir> -t <fig_title> -n <png_name>')
            sys.exit()
        elif opt in ("-a", "--geospark_dir"):
            geospark_log_dir = arg
        elif opt in ("-b", "--geomesa_dir"):
            geomesa_log_dir = arg
        elif opt in ("-c", "--arctern_dir"):
            arctern_log_dir = arg
        elif opt in ("-p", "--plot_dir"):
            plot_dir = arg
        elif opt in ("-t", "--fig_title"):
            fig_title = arg
        elif opt in ("-n", "--png_name"):
            png_name = arg


    # res_set is a list that contains historical performance data for all gis functions
    geospark_res_set, geospark_func_order = fetch_func_perf(fetch_log_files(geospark_log_dir))
    geospark_func_order = [x.lower() for x in geospark_func_order if isinstance(x, str)]
    assert len(geospark_func_order) == len(geospark_res_set)
    geospark_funcs_means_arr = []
    # produce specific result variable in main for every functions in func_order
    for i in range(0, len(geospark_func_order)):
        func_name = geospark_func_order[i]
        exec('res_{}_geospark={}'.format(func_name, geospark_res_set[i][1:]))  # ignore first item
        cur_res = (locals()['res_' + func_name + '_geospark'])
        if cur_res:
            geospark_funcs_means_arr.append(numpy.mean(cur_res))
        else:
            geospark_funcs_means_arr.append(-1)  # place holder data, this item will be delete in figure_intersection

    # res_set is a list that contains historical performance data for all gis functions
    geomesa_res_set, geomesa_func_order = fetch_func_perf(fetch_log_files(geomesa_log_dir))
    geomesa_func_order = [x.lower() for x in geomesa_func_order if isinstance(x, str)]
    assert len(geomesa_func_order) == len(geomesa_res_set)
    geomesa_funcs_means_arr = []
    # produce specific result variable in main for every functions in func_order
    for i in range(0, len(geomesa_func_order)):
        func_name = geomesa_func_order[i]
        exec('res_{}_geomesa={}'.format(func_name, geomesa_res_set[i][1:]))  # ignore first item
        cur_res = (locals()['res_' + func_name + '_geomesa'])
        if cur_res:
            geomesa_funcs_means_arr.append(numpy.mean(cur_res))
        else :
            geomesa_funcs_means_arr.append(-1)  # place holder data, this item will be delete in figure_intersection

    # res_set is a list that contains historical performance data for all gis functions
    arctern_res_set, arctern_func_order = fetch_func_perf(fetch_log_files(arctern_log_dir))
    arctern_func_order = [x.lower() for x in arctern_func_order if isinstance(x, str)]
    assert len(arctern_func_order) == len(arctern_res_set)
    arctern_funcs_means_arr = []
    # produce specific result variable in main for every functions in func_order
    for i in range(0, len(arctern_func_order)):
        func_name = arctern_func_order[i]
        exec('res_{}_arctern={}'.format(func_name, arctern_res_set[i][1:]))  # ignore first item
        cur_res = (locals()['res_' + func_name + '_arctern'])
        if cur_res:
            arctern_funcs_means_arr.append(numpy.mean(cur_res))
        else:
            arctern_funcs_means_arr.append(-1)  # place holder data, this item will be delete in figure_intersection

    res_set = []
    res_set.append(geospark_funcs_means_arr)
    res_set.append(geomesa_funcs_means_arr)
    res_set.append(arctern_funcs_means_arr)
#    intersection_funcs, intersection_res_set , geospark_remove, geomesa_remove = figure_intersection2(res_set, geospark_func_order, geomesa_func_order)
    intersection_funcs, intersection_res_set , geospark_remove, geomesa_remove,arctern_remove = figure_intersection3(res_set, geospark_func_order, geomesa_func_order,arctern_func_order)
#    plot_histogram2(intersection_funcs,intersection_res_set,png_name,fig_title)
    geospark_func_order = [x for x in geospark_func_order if x in intersection_funcs]
    geomesa_func_order = [x for x in geomesa_func_order if x in intersection_funcs]
    arctern_func_order = [x for x in arctern_func_order if x in intersection_funcs]

    intersection_res_set[0] = list(re_order(intersection_funcs,geospark_func_order,intersection_res_set[0]))
    intersection_res_set[1] = list(re_order(intersection_funcs, geomesa_func_order, intersection_res_set[1]))
    intersection_res_set[2] = list(re_order(intersection_funcs, arctern_func_order, intersection_res_set[2]))

    plot_histogram3(intersection_funcs, intersection_res_set, png_name, fig_title)
    print(geomesa_log_dir[-5:-1])
    print()
    print('geospark remove funcs:' + str(geospark_remove))
    print()
    print('geomesa remove funcs:' + str(geomesa_remove))
    print()
    print('arctern remove funcs:' + str(arctern_remove))
    print()
    print('--------------------------------------------------------------------------------------------------')
    print()




