
import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

def fetch_log_files(dir):
  log_files=[]
  func_name_list = []
  files = os.listdir(dir)
  for f in files:
    if os.path.splitext(f)[1] == '.txt':
      log_files.append(f)
      func_name_list.append(str(f).split(".")[0])
  return func_name_list, log_files

def fetch_func_perf(func_list,log_files):
  # declare var res_arrs based on func_name
  res = []
  for func_name in func_list:
    exec('res_{}=[]'.format(func_name))
  for log_file in log_files:
     tmp_arr = []
     with open(log_dir+log_file,'r') as f:
       for line in f:
         line = list(map(lambda x:x.upper(),line.split(':')))
         parser_key1 = ('geospark_'+log_file[0:-4]+'_time').upper()
         parser_key2 = ('geomesa_' + log_file[0:-4] + '_time').upper()
         parser_key3 = ('arctern_' + log_file[0:-4] + '_time').upper()
         if parser_key1 in line or parser_key2 in line or parser_key3 in line:
             tmp_arr.append(float(line[-1]))
     res.append(tmp_arr)
  return res

def perf_stability_alarm(func_name,res_func_arr):
    warning_str = ' [Warning] : The performance of ' + str(func_name) + ' fluctuates greatly!'
    # warning based on standard deviation
    std_deviation = numpy.std(res_func_arr, ddof=1)
    if std_deviation > std_threshold:
      return 1
    return 0

def plot_perf_analysis(func_name, res_func_arr):
    perf_picture = plot_dir + str(func_name) + '_perf.png'
    perf_fig_title = str(func_name) + ' Performance Fig'

    # plot
    index1 = list(range(1, len(res_func_arr)))
    plt.figure(figsize=(16, 4))  # picture size
    plt.plot(index1, res_func_arr[1:], marker='o', label="$10k$",linestyle='-', color="blue", linewidth=1)
    for a,b in zip(index1,res_func_arr):
        plt.text(a,b,round(b,3),ha='center',va='bottom',fontsize=12)
    plt.xlabel("Version ")  # X label
    plt.ylabel("Cost /ms")  # Y label
    plt.title(perf_fig_title)
    x0 = len(res_func_arr)
    y0 = res_func_arr[x0-1]
    std_deviation = numpy.std(res_func_arr[1:], ddof=1)
    mean = numpy.mean(res_func_arr[1:])
    # plt.annotate('std :%s\n'%std_deviation+'mean :%s'%mean, xy=(x0, y0), xytext=(+30, -30), textcoords='offset points', fontsize=12,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    plt.text(x0,y0,'std :%s\n'%round(std_deviation,5)+'mean :%s'%round(mean,5),bbox=dict(facecolor='g', edgecolor='gray', alpha=0.1),fontsize=14)
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


func_list_arr = [
    'ST_Area',
    'ST_AsText',
    'ST_Buffer',
    'ST_Centriod',
    'ST_Contains',
    'ST_Crosses',
    'ST_Distance',
    'ST_Envelope',
    'ST_Equals',
    'ST_GeometryType',
    'ST_GeomFromWKT',
    'ST_Intersects',
    'ST_IsSimple',
    'ST_IsValid',
    'ST_Length',
    'ST_LineStringFromText',
    'ST_NPoints',
    'ST_Overlaps',
    'ST_PointFromText',
    'ST_Point',
    'ST_PolygonFromText',
    'ST_Touches',
    'ST_WithIn'
    ]
log_dir = 'geomesa_report2/10_8/'
plot_dir = 'geomesa_report2/pix_10_8/'
# Performance analysis standard deviation accuracy tolerance
std_threshold = 3.0

# main invocation
if __name__ == "__main__":
    # res_set is a list that contains historical performance data for all gis functions
    func_name_list, log_files = fetch_log_files(log_dir)
    res_set = fetch_func_perf(func_name_list,log_files)

    for i in range(0,len(func_name_list)):
      func_name = func_name_list[i]
      exec('res_{}={}'.format(func_name,res_set[i]))

    alarm_num = 0
    plot_num = 0
    plot_failed_func = []
    alarm_func = []
    for func_name in func_name_list:
      res_arr = 'res_' + func_name
      # plot
      cur_res_arr = locals()[res_arr]
      if cur_res_arr:
          print(cur_res_arr)
          print(func_name)
          plot_perf_analysis(func_name,cur_res_arr)
          plot_num = plot_num + 1
          # performance test stability
          if perf_stability_alarm(func_name, locals()[res_arr]):
              alarm_num = alarm_num + 1
              alarm_func.append(func_name)
      else :
          plot_failed_func.append(func_name)


    print('Plot %s performance analyze Fig.'%plot_num)
    print('Plot failed functions list :%s '%plot_failed_func)
    print('There are %s functions alarming!'%alarm_num)
    print('Alarm functions list :%s '%alarm_func)
    # specific funciton test examples
    #plot_perf_analysis('st_within',res_st_within)
    #perf_stability_alarm('st_within',res_st_within)
