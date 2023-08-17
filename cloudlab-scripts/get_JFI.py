import pandas as pd
import numpy as np
import csv
import sys
import os

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
sender=int(sys.argv[1])
num_clients=int(sys.argv[2])
cca1=sys.argv[3]
duration=int(sys.argv[4])
delay=int(sys.argv[5])

ports=[]
y_values=[]
sq_y_values=[]
   
jfi_filename='/local/repository/cloudlab-scripts/jfi.csv'
if not os.path.isfile(jfi_filename):
    with open(jfi_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header ='CCA', 'Duration of Expt(sec)', 'Base RTT(ms)', 'Total Bandwidth(Kbps)', 'Sum of sq of BW', 'Flow Count', 'JFI'
      writer.writerow(header)


for i in range (0,sender):
  dat_iperf= pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )
  port_un=pd.unique(dat_iperf.port)
  count_port=len(port_un)
  ports.append(count_port)
  for p in port_un:
    dat_flow_iperf=dat_iperf[dat_iperf.port==p]
    bandwidth_port=pd.to_numeric(dat_flow_iperf['bitrate'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    sq_bandwidth_port= bandwidth_port*bandwidth_port
    if not np.isnan(bandwidth_port):
      y_values.append(bandwidth_port)
      sq_y_values.append(sq_bandwidth_port)

with open(jfi_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  columns = cca1, duration, delay, sum(y_values),sum(sq_y_values), sum(ports), sum(y_values)*sum(y_values)/(sum(sq_y_values)*sum(ports))
  writer.writerow(columns)




