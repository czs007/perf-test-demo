#!/bin/bash -e
python perf_analyze.py -a /home/czp/performance/geospark_log/10_5/ -b /home/czp/performance/geomesa_log/10_5/ -c /home/czp/performance/arctern_log/10_5/ -p /home/czp/performance/picture/ -n 10_5 > /home/czp/performance/picture/log.txt
python perf_analyze.py -a /home/czp/performance/geospark_log/10_6/ -b /home/czp/performance/geomesa_log/10_6/ -c /home/czp/performance/arctern_log/10_6/ -p /home/czp/performance/picture/ -n 10_6 >> /home/czp/performance/picture/log.txt
python perf_analyze.py -a /home/czp/performance/geospark_log/10_7/ -b /home/czp/performance/geomesa_log/10_7/ -c /home/czp/performance/arctern_log/10_7/ -p /home/czp/performance/picture/ -n 10_7 >> /home/czp/performance/picture/log.txt
python perf_analyze.py -a /home/czp/performance/geospark_log/10_8/ -b /home/czp/performance/geomesa_log/10_8/ -c /home/czp/performance/arctern_log/10_8/ -p /home/czp/performance/picture/ -n 10_8 >> /home/czp/performance/picture/log.txt
python perf_analyze.py -a /home/czp/performance/geospark_log/10_9/ -b /home/czp/performance/geomesa_log/10_9/ -c /home/czp/performance/arctern_log/10_9/ -p /home/czp/performance/picture/ -n 10_9 >> /home/czp/performance/picture/log.txt
