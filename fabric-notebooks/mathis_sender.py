import pandas as pd
import numpy as np
import csv
import sys
import os

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
i=int(sys.argv[1])
num_clients=int(sys.argv[2])
cca1=sys.argv[3]
dropped=int(sys.argv[4])
sent=int(sys.argv[5])
time_interval=float(sys.argv[6])
duration=int(sys.argv[7])

list_cwnd_half=[]
ports=[]
y_values=[]

x1_values=[]
x2_values=[]
list_retrans=[]
list_ratio=[]


csv_filename="packet_loss_iperf"+str(i)+".csv"
if not os.path.isfile(csv_filename):
    with open(csv_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'port', 'mean_rtt', 'bandwidth_port', 'port_retrans', 'cwn_half_port', 'packet_loss', 'x1', 'cwnd_half_rate','x2','ratio'
      writer.writerow(header)


dat_rtt = pd.read_csv("data-cwn-10.10.2.1"+str(i)+"-file.txt",header=None, names=['port', 'cwnd' , 'rtt'])
dat_cwn = pd.read_csv("data-cwn-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port','cwnd'])
dat_iperf= pd.read_csv("data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )
port_un=pd.unique(dat_cwn.port)
count_port=len(port_un)
ports.append(count_port)
for p in port_un:
    dat_flow = dat_cwn[dat_cwn.port==p]
    dat_flow_iperf=dat_iperf[dat_iperf.port==p]
    dat_flow_rtt=dat_rtt[dat_rtt.port==p]
    #calculate congestion window halving events

    x = dat_flow.cwnd.diff().values
    x[np.where(x==0)] = 1
    cwn_half_port=np.sum((np.diff(np.sign(x))) == -2)
    list_cwnd_half.append(cwn_half_port)

    mean_rtt=np.nanmean(dat_flow_rtt['rtt'])

    #method-1: calculation of packet_loss rate using transfer and retrans from iperf3 data

    if dat_flow_iperf.shape[0] > 0 :
      exponent=9 if dat_flow_iperf['transfer_unit'].iloc[0]=='GBytes' else 6
    port_retrans=pd.to_numeric(dat_flow_iperf['retrans'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    transfered_data=pd.to_numeric(dat_flow_iperf['transfer'].iloc[0])*pow(10,exponent) if dat_flow_iperf.shape[0] > 0 else np.nan
    packet_loss=(port_retrans*1500)/(transfered_data)
    list_retrans.append(port_retrans)
    x1=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss))


    #method-2: calculation of cwnd_halving rate using transfer from iperf3 data
    if cwn_half_port:
      cwnd_half_rate=(cwn_half_port*1500)/(transfered_data)
      x2=(1448*8*1000)/(mean_rtt*np.sqrt(cwnd_half_rate))

      ratio=port_retrans/cwn_half_port
      list_ratio.append(ratio)
    bandwidth_port=pd.to_numeric(dat_flow_iperf['bitrate'].iloc[0]*1000) if dat_flow_iperf.shape[0] > 0 else np.nan

    if not np.isnan(bandwidth_port):
      x1_values.append(x1)
      x2_values.append(x2)
      y_values.append(bandwidth_port)
      with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        columns = p, mean_rtt, bandwidth_port, port_retrans, cwn_half_port, packet_loss, x1, cwnd_half_rate, x2, ratio
        writer.writerow(columns)









