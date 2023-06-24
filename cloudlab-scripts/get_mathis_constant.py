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

x2_values=[]
x3_values=[]


list_retrans2=[]

list_ratio2=[]


csv_filename="/local/repository/cloudlab-scripts/packet_loss.csv"
if not os.path.isfile(csv_filename):
    with open(csv_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'port', 'data_seg_out', 'mean_rtt', 'bandwidth_port', 'port_retrans1', 'port_retrans2', 'cwn_half_port', 'packet_loss1', 'x1', 'packet_loss2', 'x2', 'cwnd_half_rate1','x3', 'cwnd_half_rate2', 'x4', 'ratio1', 'ratio2'
      writer.writerow(header)
   
output_filename='/local/repository/cloudlab-scripts/output_mathis_C.csv'
if not os.path.isfile(output_filename):
    with open(output_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'total_ports', 'ports', 'sum(y_values)', 'total_cwnd_half', 'total_retransmission1', 'total_retransmission2', 'total_retransmission1/total_cwnd_half', 'total_retransmission2/total_cwnd_half', 'np.nanmean(list_ratio1)', 'np.nanmean(list_ratio2)', 'reg_simple1.intercept_', 'reg_simple1.coef_[0]', 'reg_simple2.intercept_', 'reg_simple2.coef_[0]', 'reg_simple3.intercept_', 'reg_simple3.coef_[0]', 'reg_simple4.intercept_', 'reg_simple4.coef_[0]', 'router_dropped', 'router_sent', 'router_dropped/total_cwnd_half'
      writer.writerow(header)


for i in range (0,10):
  dat_cwn = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/data-cwn-10.10.2.1"+str(i)+"-file.txt", header=None, names=['port', 'cwnd', 'rtt'])
  dat_iperf= pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/data-iperf-10.10.2.1"+str(i)+".csv", header=None, names=['id','port','duration','time_unit','transfer_data','data_unit','bandwidth','BW_unit','retrans'] )
  port_un=pd.unique(dat_cwn.port)
  count_port=len(port_un)
  ports.append(count_port)
  for p in port_un:
    dat_flow = dat_cwn[dat_cwn.port==p]
    dat_flow_iperf=dat_iperf[dat_iperf.port==p]
    #calculate congestion window halving events

    x = dat_flow.cwnd.diff().values
    x[np.where(x==0)] = 1
    cwn_half_port=np.sum((np.diff(np.sign(x))) == -2)
    list_cwnd_half.append(cwn_half_port)

    meas_rtt=dat_flow['rtt']
    mean_rtt=np.nanmean(pd.to_numeric(meas_rtt))

    #method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data
    if dat_flow_iperf.shape[0] > 0 :
      exponent=9 if dat_flow_iperf['data_unit'].iloc[0]=='GBytes' else 6
    port_retrans2=pd.to_numeric(dat_flow_iperf['retrans'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    transfered_data=pd.to_numeric(dat_flow_iperf['transfer_data'].iloc[0])*pow(10,exponent) if dat_flow_iperf.shape[0] > 0 else np.nan
    packet_loss2=(port_retrans2*1500)/(transfered_data)
    list_retrans2.append(port_retrans2)
    x2=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss2))


    #method-3: calculation of cwnd_halving rate using transfer from iperf3 data
    if cwn_half_port:
      cwnd_half_rate1=(cwn_half_port*1500)/(transfered_data)
      x3=(1448*8*1000)/(mean_rtt*np.sqrt(cwnd_half_rate1))

      ratio2=port_retrans2/cwn_half_port
      list_ratio2.append(ratio2)
    bandwidth_port=pd.to_numeric(dat_flow_iperf['bandwidth'].iloc[0])*1000 if dat_flow_iperf.shape[0] > 0 else np.nan

    if not np.isnan(bandwidth_port):
      x2_values.append(x2)
      x3_values.append(x3)
      y_values.append(bandwidth_port)
      with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        columns = p, mean_rtt, bandwidth_port, port_retrans2, cwn_half_port, packet_loss2, x2, cwnd_half_rate1, x3, ratio2
        writer.writerow(columns)

total_cwnd_half=np.nansum(list_cwnd_half)
total_retransmission2=np.nansum(list_retrans2)
print(total_cwnd_half)

print(sum(ports))

print(total_retransmission2)

print(total_retransmission2/total_cwnd_half)

print(np.nanmean(list_ratio2))


sns.set()

y_values = np.array(y_values)

x2_values = np.array(x2_values).reshape(-1, 1)
x3_values = np.array(x3_values).reshape(-1, 1)




print("method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data")
reg_simple2 = LinearRegression(fit_intercept = False).fit(x2_values, y_values)
print("Intercept: " , reg_simple2.intercept_)
print("Coefficient list: ", reg_simple2.coef_)

print("method-3: calculation of cwnd_halving rate using transfer from iperf3 data")
reg_simple3 = LinearRegression(fit_intercept = False).fit(x3_values, y_values)
print("Intercept: " , reg_simple3.intercept_)
print("Coefficient list: ", reg_simple3.coef_)




with open(output_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  columns = sum(ports), len(y_values), sum(y_values), total_cwnd_half, total_retransmission2, total_retransmission2/total_cwnd_half, np.nanmean(list_ratio2), reg_simple2.intercept_, reg_simple2.coef_[0], reg_simple3.intercept_, reg_simple3.coef_[0], dropped, sent, dropped/total_cwnd_half
  writer.writerow(columns)


y_hat2 = reg_simple2.predict(x2_values)

y_hat3 = reg_simple3.predict(x3_values)



with PdfPages("/local/repository/cloudlab-scripts/linear_reg_plot.pdf") as pdf:
  plt.rcParams['figure.figsize'] = (8,6)



  plt.scatter(x=x2_values.squeeze(), y=y_values, color='C4', s=10, label='actual values')
  plt.scatter(x=x2_values.squeeze(), y=y_hat2, color='C3', s=10, label='predicted_values')
  plt.plot(x2_values.squeeze(), y_hat2, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)") 
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x3_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x3_values.squeeze(), y=y_hat3, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x3_values.squeeze(), y_hat3, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(cwnd_half_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-3: calculation of cwnd_halving rate using transfer from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()
