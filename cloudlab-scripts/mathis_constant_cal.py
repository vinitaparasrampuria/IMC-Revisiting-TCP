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
duration=int(sys.argv[6])

list_cwnd_half=[]
ports=[]
y_values=[]
x1_values=[]
x2_values=[]
x3_values=[]
x4_values=[]
x5_values=[]
x6_values=[]
list_retrans_ss=[]
list_retrans_iperf=[]
list_ratio_ss=[]
list_ratio_iperf=[]


csv_filename="packet_loss.csv"
if not os.path.isfile(csv_filename):
    with open(csv_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'port', 'data_seg_out', 'mean_rtt', 'bandwidth_port', 'retrans_ss', 'retrans_iperf', 'cwn_half_port', 'packet_loss1', 'x1', 'packet_loss2', 'x2', 'packet_loss3', 'x3', 'packet_loss4', 'x4', 'cwnd_half_rate_ss','x5', 'cwnd_half_rate_iperf', 'x6', 'ratio_ss', 'ratio_iperf'
      writer.writerow(header)
   
output_filename='output_mathis_C.csv'
if not os.path.isfile(output_filename):
    with open(output_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'time_duration', 'ports', 'sum(y_values)', 'total_cwnd_half', 'total_retransmission_ss', 'total_retransmission_iperf', 'total_retransmission_ss/total_cwnd_half', 'total_retransmission_iperf/total_cwnd_half', 'np.nanmean(list_ratio_ss)', 'np.nanmean(list_ratio_iperf)', 'reg_simple1.intercept_', 'reg_simple1.coef_[0]', 'reg_simple2.intercept_', 'reg_simple2.coef_[0]', 'reg_simple3.intercept_', 'reg_simple3.coef_[0]', 'reg_simple4.intercept_', 'reg_simple4.coef_[0]','reg_simple5.intercept_', 'reg_simple5.coef_[0]','reg_simple6.intercept_', 'reg_simple6.coef_[0]', 'router_dropped', 'router_sent', 'router_dropped/total_cwnd_half', 'mdape1', 'mdape2', 'mdape3','mdape4', 'mdape5', 'mdape6'
      writer.writerow(header)


for i in range (0,1):
  dat_ss = pd.read_csv("data-cwn-10.10.2.1"+str(i)+"-file.txt", header=None, names=['port', 'cwnd','rtt','data_seg','retrans'])
  dat_cwn_iperf = pd.read_csv("data-cwn-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port','cwnd'])
  dat_retrans_iperf= pd.read_csv("data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )
    
  port_un=pd.unique(dat_cwn_iperf.port)
  count_port=len(port_un)
  ports.append(count_port)
  for p in port_un:
    dat_flow = dat_cwn_iperf[dat_cwn_iperf.port==p]
    dat_flow_iperf=dat_retrans_iperf[dat_retrans_iperf.port==p]
    dat_flow_ss=dat_ss[dat_ss.port==p]
    #calculate congestion window halving events

    x = dat_flow.cwnd.diff().values
    x[np.where(x==0)] = 1
    cwn_half_port=np.sum((np.diff(np.sign(x))) == -2)
    list_cwnd_half.append(cwn_half_port)

    #method-1: calculation of packet_loss rate using data_seg_out from ss and retrans from ss data
    data_seg_out=dat_flow_ss['data_seg'].iloc[len(dat_flow) - 1]   
    mean_rtt=np.nanmean(dat_flow_ss['rtt'])
    retrans_ss=dat_flow_ss['retrans'].iloc[len(dat_flow) - 1]
    list_retrans_ss.append(retrans_ss)
    packet_loss1=retrans_ss/data_seg_out
    if packet_loss1>0:
      x1=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss1))


    # method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data
    if dat_flow_iperf.shape[0] > 0 :
      exponent=9 if dat_flow_iperf['transfer_unit'].iloc[0]=='GBytes' else 6
    retrans_iperf=pd.to_numeric(dat_flow_iperf['retrans'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    transfered_data=pd.to_numeric(dat_flow_iperf['transfer'].iloc[0])*pow(10,exponent) if dat_flow_iperf.shape[0] > 0 else np.nan
    packet_loss2=(retrans_iperf*1500)/(transfered_data)
    list_retrans_iperf.append(retrans_iperf)
    x2=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss2))

     # method-3: calculation of packet_loss rate using transfer data from iperf and retrans from ss data
    packet_loss3=(retrans_ss*1500)/(transfered_data)
    x3=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss3))

    # method-4: calculation of packet_loss rate using data_seg_out from ss and retrans from iperf data
    packet_loss4=retrans_iperf/data_seg_out
    x4=(1448*8*1000)/(mean_rtt*np.sqrt(packet_loss4))
    

    #method-5: calculation of cwnd_halving rate using transfer from iperf3 data
    if cwn_half_port:
      cwnd_half_rate_ss=(cwn_half_port*1500)/(transfered_data)
      x5=(1448*8*1000)/(mean_rtt*np.sqrt(cwnd_half_rate_ss))

    #method-6: calculation of cwnd_halving rate using data_seg_out from ss data
      cwnd_half_rate_iperf=cwn_half_port/data_seg_out
      x6=(1448*8*1000)/(mean_rtt*np.sqrt(cwnd_half_rate_iperf))

      ratio_ss=retrans_ss/cwn_half_port
      ratio_iperf=retrans_iperf/cwn_half_port
      list_ratio_ss.append(ratio_ss)
      list_ratio_iperf.append(ratio_iperf)
    bandwidth_port=pd.to_numeric(dat_flow_iperf['bitrate'].iloc[0])*1000 if dat_flow_iperf.shape[0] > 0 else np.nan

    if not np.isnan(bandwidth_port):
      x1_values.append(x1)
      x2_values.append(x2)
      x3_values.append(x3)
      x4_values.append(x4)
      x5_values.append(x5)
      x6_values.append(x6)
      y_values.append(bandwidth_port)
      with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        columns = p, data_seg_out, mean_rtt, bandwidth_port, retrans_ss, retrans_iperf, cwn_half_port, packet_loss1, x1, packet_loss2, x2, packet_loss3, x3, packet_loss4, x4, cwnd_half_rate_ss, x5, cwnd_half_rate_iperf, x6, ratio_ss, ratio_iperf
        writer.writerow(columns)

total_cwnd_half=np.nansum(list_cwnd_half)
total_retransmission_ss=np.nansum(retrans_ss)
total_retransmission_iperf=np.nansum(retrans_iperf)
print(total_cwnd_half)

print(sum(ports))

print(total_retransmission_ss)
print(total_retransmission_iperf)

print(total_retransmission_ss/total_cwnd_half)
print(total_retransmission_iperf/total_cwnd_half)

print(np.nanmean(list_ratio_ss))
print(np.nanmean(list_ratio_iperf))


sns.set()
x1_values = np.array(x1_values).reshape(-1, 1)
y_values = np.array(y_values)

x2_values = np.array(x2_values).reshape(-1, 1)
x3_values = np.array(x3_values).reshape(-1, 1)
x4_values = np.array(x4_values).reshape(-1, 1)
x5_values = np.array(x5_values).reshape(-1, 1)
x6_values = np.array(x6_values).reshape(-1, 1)


reg_simple1 = LinearRegression(fit_intercept = False).fit(x1_values, y_values)
print("method-1: calculation of packet_loss rate using data_seg_out from ss and retrans from ss data")
print("Intercept: " , reg_simple1.intercept_)
print("Coefficient list: ", reg_simple1.coef_)


print("method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data")
reg_simple2 = LinearRegression(fit_intercept = False).fit(x2_values, y_values)
print("Intercept: " , reg_simple2.intercept_)
print("Coefficient list: ", reg_simple2.coef_)

print("method-3: calculation of packet_loss rate using transfer data from iperf and retrans from ss data")
reg_simple3 = LinearRegression(fit_intercept = False).fit(x3_values, y_values)
print("Intercept: " , reg_simple3.intercept_)
print("Coefficient list: ", reg_simple3.coef_)

print("method-4: calculation of packet_loss rate using data_seg_out from ss and retrans from iperf data")
reg_simple4 = LinearRegression(fit_intercept = False).fit(x4_values, y_values)
print("Intercept: " , reg_simple4.intercept_)
print("Coefficient list: ", reg_simple4.coef_)

print("method-5: calculation of cwnd_halving rate using transfer from iperf3 data")
reg_simple5 = LinearRegression(fit_intercept = False).fit(x5_values, y_values)
print("Intercept: " , reg_simple5.intercept_)
print("Coefficient list: ", reg_simple5.coef_)

print("method-6: calculation of cwnd_halving rate using data_seg_out from ss data")
reg_simple6 = LinearRegression(fit_intercept = False).fit(x6_values, y_values)
print("Intercept: " , reg_simple6.intercept_)
print("Coefficient list: ", reg_simple6.coef_)

y_hat1 = reg_simple1.predict(x1_values)

y_hat2 = reg_simple2.predict(x2_values)

y_hat3 = reg_simple3.predict(x3_values)

y_hat4 = reg_simple4.predict(x4_values)

y_hat5 = reg_simple5.predict(x5_values)

y_hat6 = reg_simple6.predict(x6_values)

mdape1=np.median((np.abs(np.subtract(y_values, y_hat1)/ y_values))) * 100
mdape2=np.median((np.abs(np.subtract(y_values, y_hat2)/ y_values))) * 100
mdape3=np.median((np.abs(np.subtract(y_values, y_hat3)/ y_values))) * 100
mdape4=np.median((np.abs(np.subtract(y_values, y_hat4)/ y_values))) * 100
mdape5=np.median((np.abs(np.subtract(y_values, y_hat5)/ y_values))) * 100
mdape6=np.median((np.abs(np.subtract(y_values, y_hat6)/ y_values))) * 100



with open(output_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)   
  columns = duration, sum(ports), sum(y_values), total_cwnd_half, total_retransmission_ss, total_retransmission_iperf, total_retransmission_ss/total_cwnd_half, total_retransmission_iperf/total_cwnd_half, np.nanmean(list_ratio_ss), np.nanmean(list_ratio_iperf), reg_simple1.intercept_, reg_simple1.coef_[0], reg_simple2.intercept_, reg_simple2.coef_[0], reg_simple3.intercept_, reg_simple3.coef_[0], reg_simple4.intercept_, reg_simple4.coef_[0], reg_simple5.intercept_, reg_simple5.coef_[0], reg_simple6.intercept_, reg_simple6.coef_[0], dropped, sent, dropped/total_cwnd_half, mdape1, mdape2, mdape3, mdape4, mdape5, mdape6
  writer.writerow(columns)




with PdfPages("linear_reg_plot.pdf") as pdf:
  plt.rcParams['figure.figsize'] = (8,6)

  plt.scatter(x=x1_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x1_values.squeeze(), y=y_hat1, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x1_values.squeeze(), y_hat1, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)") 
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-1 calculation of packet_loss rate using data_seg_out from ss and retrans from ss data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

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
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-3: calculation of packet_loss rate using transfer data from iperf and retrans from ss data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x4_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x4_values.squeeze(), y=y_hat4, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x4_values.squeeze(), y_hat4, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-4: calculation of packet_loss rate using data_seg_out from ss and retrans from iperf data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x5_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x5_values.squeeze(), y=y_hat5, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x5_values.squeeze(), y_hat5, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(cwnd_half_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-5: calculation of cwnd_halving rate using transfer from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x6_values.squeeze(), y=y_values, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x6_values.squeeze(), y=y_hat6, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x6_values.squeeze(), y_hat6, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(cwnd_half_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")

  plt.title("Method-6: calculation of cwnd_halving rate using data_seg_out from ss data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()


