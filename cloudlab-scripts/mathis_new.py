from pandas.core.indexes.datetimes import date_range
import pandas as pd
import numpy as np
import csv
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
sender=int(sys.argv[1])
num_clients=int(sys.argv[2])
cca1=sys.argv[3]
dropped=int(sys.argv[4])
sent=int(sys.argv[5])

list_cwnd_half=[]
ports=[]
y_values=[]

x1_values=[]
x2_values=[]
list_retrans=[]
list_ratio=[]


csv_filename="/local/repository/cloudlab-scripts/packet_loss_iperf.csv"
if not os.path.isfile(csv_filename):
    with open(csv_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'port', 'mean_rtt', 'bandwidth_port', 'port_retrans', 'cwn_half_port', 'packet_loss', 'x1', 'cwnd_half_rate','x2','ratio'
      writer.writerow(header)
   
output_filename='/local/repository/cloudlab-scripts/output_mathis_C_iperf.csv'
if not os.path.isfile(output_filename):
    with open(output_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'ports', 'sum(y_values)', 'total_cwnd_half', 'total_retransmission', 'total_retransmission/total_cwnd_half', 'np.nanmean(list_ratio)', 'reg_simple1.intercept_', 'reg_simple1.coef_[0]', 'reg_simple2.intercept_', 'reg_simple2.coef_[0]', 'router_dropped', 'router_sent', 'router_dropped/total_cwnd_half'
      writer.writerow(header)


for i in range (0,sender):
  dat_rtt = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/"data-cwn-10.10.2.1"+str(i)+"-file.txt",header=None, names=['port', 'cwnd' , 'rtt'])
  dat_cwn = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/data-cwn-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port','cwnd'])
  dat_iperf= pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )
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

    #method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data

    if dat_flow_iperf.shape[0] > 0 :
      exponent=9 if dat_flow_iperf['transfer_unit'].iloc[0]=='GBytes' else 6
    port_retrans=pd.to_numeric(dat_flow_iperf['retrans'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    transfered_data=pd.to_numeric(dat_flow_iperf['transfer'].iloc[0])*pow(10,exponent) if dat_flow_iperf.shape[0] > 0 else np.nan
    packet_loss=(port_retrans*1500)/(transfered_data)
    list_retrans.append(port_retrans)
    x1=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss))


    #method-3: calculation of cwnd_halving rate using transfer from iperf3 data
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

total_cwnd_half=np.nansum(list_cwnd_half)
total_retransmission=np.nansum(list_retrans)
print(total_cwnd_half)

print(sum(ports))
print(total_retransmission)
print(total_retransmission/total_cwnd_half)
print(np.nanmean(list_ratio))

sns.set()

y_values = np.array(y_values)
x1_values = np.array(x1_values).reshape(-1, 1)
x2_values = np.array(x2_values).reshape(-1, 1)




print("method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data")
reg_simple1 = LinearRegression(fit_intercept = False).fit(x1_values, y_values)
print("Intercept: " , reg_simple1.intercept_)
print("Coefficient list: ", reg_simple1.coef_)

print("method-3: calculation of cwnd_halving rate using transfer from iperf3 data")
reg_simple2 = LinearRegression(fit_intercept = False).fit(x2_values, y_values)
print("Intercept: " , reg_simple2.intercept_)
print("Coefficient list: ", reg_simple2.coef_)


with open(output_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  columns = sum(ports), sum(y_values), total_cwnd_half, total_retransmission, total_retransmission/total_cwnd_half, np.nanmean(list_ratio), reg_simple1.intercept_, reg_simple1.coef_[0], reg_simple2.intercept_, reg_simple2.coef_[0], dropped, sent, dropped/total_cwnd_half
  writer.writerow(columns)


y_hat1 = reg_simple1.predict(x1_values)

y_hat2 = reg_simple2.predict(x2_values)


with PdfPages("/local/repository/cloudlab-scripts/linear_reg_plot.pdf") as pdf:
  plt.rcParams['figure.figsize'] = (8,6)


  plt.scatter(x=x1_values.squeeze(), y=y_values, color='C4', s=10, label='actual values')
  plt.scatter(x=x1_values.squeeze(), y=y_hat1, color='C3', s=10, label='predicted_values')
  plt.plot(x1_values.squeeze(), y_hat1, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)") 
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-1: calculation of packet_loss rate using transfer and retrans from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x2_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x2_values.squeeze(), y=y_hat2, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x2_values.squeeze(), y_hat2, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(cwnd_half_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-2: calculation of cwnd_halving rate using transfer from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()
