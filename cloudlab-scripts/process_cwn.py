from pandas.core.indexes.datetimes import date_range
import pandas as pd
import numpy as np
import csv
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import sys

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
senders=int(sys.argv[1])
cca1=sys.argv[2]

ports=[]

y_values=[]
x_values=[]
x2_values=[]
x3_values=[]
x4_values=[]
csv_filename="/local/repository/cloudlab-scripts/result-"+cca1+"/packet_loss.csv"
for i in range (0,senders):
  dat = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/sender-cwn-10.10.2.1"+str(i)+"-file.txt", header=None, names=['port', 'cwnd','rtt','data_seg','retrans'])
  dat_iperf= pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca1+"/output-10.10.2.1"+str(i)+".csv", header=None, names=['id','port','duration','time_unit','transfer_data','data_unit','bandwidth','BW_unit','retrans'] )
  port_un=pd.unique(dat.port)

  for p in port_un:
    dat_flow = dat[dat.port==p]
    dat_flow_iperf=dat_iperf[dat_iperf.port==p]
    x = dat_flow.cwnd.diff().values
    x[np.where(x==0)] = 1
    cwn_port_half=np.sum((np.diff(np.sign(x))) == -2)
    
    #method-1
    data_seg_out=dat_flow['data_seg'].iloc[len(dat_flow) - 1]
    meas_rtt=dat_flow['rtt']
    #print(meas_rtt)
    avg_rtt1 = meas_rtt.str.split('/').str[0]
    avg_rtt=np.nanmean(pd.to_numeric(avg_rtt1))

    meas_retrans=dat_flow['retrans'].iloc[len(dat_flow) - 1]
    total_retrans = int(meas_retrans.split('/')[1]) if pd.notnull(meas_retrans) else meas_retrans

    bandwidth_port=pd.to_numeric(dat_flow_iperf['bandwidth'].iloc[0])*1000 if dat_flow_iperf.shape[0] > 0 else np.nan
    #print((bandwidth_port))
    #print(dat_flow_iperf)
    #print(p)
    #print(data_seg_out)
    #print(meas_rtt)
    #print(avg_rtt)
    #print(meas_retrans)
    #print(total_retrans)
    packet_drop=total_retrans/data_seg_out
    #print(packet_drop)
    #print('------')
    
    packet_drop=total_retrans/data_seg_out
    #print(packet_drop)

    x1=(1448*8*1000)/(avg_rtt*np.sqrt(packet_drop))

  
    #method-2


    retrans2=pd.to_numeric(dat_flow_iperf['retrans'].iloc[0]) if dat_flow_iperf.shape[0] > 0 else np.nan
    transfered_data=pd.to_numeric(dat_flow_iperf['transfer_data'].iloc[0])*pow(10,9) if dat_flow_iperf.shape[0] > 0 else np.nan
    packet_loss2=(retrans2*1500)/(transfered_data)
    #print(retrans2)
    #print(packet_loss1)
    #print(avg_rtt)

    x2=(1448*8*1000)/(avg_rtt*np.sqrt(packet_loss2))
    #print(x2)

    #method-3

    packet_loss3=(cwn_port_half*1500)/(transfered_data)
    x3=(1448*8*1000)/(avg_rtt*np.sqrt(packet_loss3))

    #method-4
    packet_loss4=cwn_port_half/data_seg_out
    if packet_loss4:
      x4=(1448*8*1000)/(avg_rtt*np.sqrt(packet_loss4))


    #print('---')
    if not np.isnan(bandwidth_port):
      x_values.append(x1)
      y_values.append(bandwidth_port)
      x2_values.append(x2)
      x3_values.append(x3)
      x4_values.append(x4)

x_values = np.array(x_values).reshape(-1, 1)
y_values = np.array(y_values)

x2_values = np.array(x2_values).reshape(-1, 1)
x3_values = np.array(x3_values).reshape(-1, 1)
x4_values = np.array(x4_values).reshape(-1, 1)


reg_simple = LinearRegression().fit(x_values, y_values)   
print("method-1: calculation of packet_loss rate using data_seg_out and retrans from ss data") 
print("Intercept: " , reg_simple.intercept_)
print("Coefficient list: ", reg_simple.coef_)

print("method-2: calculation of packet_loss rate using transfer and retrans from iperf3 data") 
reg_simple = LinearRegression().fit(x2_values, y_values)    
print("Intercept: " , reg_simple.intercept_)
print("Coefficient list: ", reg_simple.coef_)

print("method-3: calculation of cwnd_halving rate using transfer from iperf3 data") 
reg_simple = LinearRegression().fit(x3_values, y_values)    
print("Intercept: " , reg_simple.intercept_)
print("Coefficient list: ", reg_simple.coef_)

print("method-4: calculation of cwnd_halving rate using data_seg_out from ss data") 
reg_simple = LinearRegression().fit(x4_values, y_values)    
print("Intercept: " , reg_simple.intercept_)
print("Coefficient list: ", reg_simple.coef_)
