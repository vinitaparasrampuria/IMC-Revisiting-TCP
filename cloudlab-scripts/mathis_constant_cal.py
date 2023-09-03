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
cca=sys.argv[3]
n_seg_dropped=int(sys.argv[4])
n_seg_sent=int(sys.argv[5])
duration=int(sys.argv[6])
rtt=int(sys.argv[7])


dat_exp = pd.DataFrame( columns=['port',
                           'data_seg',
                           'retrans_ss',
                           'rtt',
                           'bitrate',
                           'retrans_iperf']
 )

for i in range (0,sender):
  dat_ss = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca+"/data-cwn-10.10.2.1"+str(i)+"-file.txt", header=None, names=['port', 'cwnd','rtt','data_seg','retrans'])
  dat_cwn_iperf = pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca+"/data-cwn-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port','cwnd'])
  dat_retrans_iperf= pd.read_csv("/local/repository/cloudlab-scripts/result-"+cca+"/data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )

  ss_out=dat_ss.groupby("port",as_index=False).agg({'data_seg':['max'], 'retrans':['max'], 'rtt': ['mean']})
  ss_out.columns=['port','data_seg', 'retrans', 'rtt']
  dat_combo = ss_out.merge(dat_retrans_iperf[['port', 'bitrate', 'retrans']], on='port', how='inner', suffixes=['_ss', '_iperf'])
  dat_combo['cwnd_halve'] = -1

  port_un=pd.unique(dat_combo.port)
  for p in port_un:
    dat_flow = dat_cwn_iperf[dat_cwn_iperf.port==p]
    #calculate congestion window halving events
    x = dat_flow.cwnd.diff().values
    x = x[x!=0]
    cwn_half_port=np.sum((np.diff(np.sign(x))) == -2)
    dat_combo.loc[dat_combo['port']==p, 'cwnd_halve']=cwn_half_port

  dat_exp  = pd.concat([dat_exp, dat_combo], ignore_index=True)
dat_exp=dat_exp.convert_dtypes()
dat_exp['retrans_iperf'] = pd.to_numeric(dat_exp['retrans_iperf'], errors='coerce').fillna(0)
dat_exp = dat_exp.assign(p_ss_retrans = dat_exp['retrans_ss']/dat_exp['data_seg'])
dat_exp = dat_exp.assign(p_iperf_retrans = dat_exp['retrans_iperf']/dat_exp['data_seg'])
dat_exp = dat_exp.assign(p_cwnd_halve = dat_exp['cwnd_halve']/dat_exp['data_seg'])
dat_exp = dat_exp.assign(p_router_drop = n_seg_dropped/n_seg_sent )

np.sqrt(np.array([4, 9, 25]))
print(dat_exp.info())

coef_retrans_ss    = LinearRegression(fit_intercept = False).fit(
  ( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_ss_retrans'].values) ) ).values.reshape(-1,1), 
  dat_exp['bitrate']*1000.0
).coef_
coef_retrans_iperf = LinearRegression(fit_intercept = False).fit(
  ( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_iperf_retrans'].values) ) ).values.reshape(-1,1), 
  dat_exp['bitrate']*1000.0
).coef_
coef_cwnd_halve    = LinearRegression(fit_intercept = False).fit(
  ( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_cwnd_halve'].values) ) ).values.reshape(-1,1), 
  dat_exp['bitrate']*1000.0
).coef_
coef_router_dropped = LinearRegression(fit_intercept = False).fit(
  ( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_router_drop'].values) ) ).values.reshape(-1,1), 
  dat_exp['bitrate']*1000.0
).coef_
print(coef_retrans_ss, coef_retrans_iperf, coef_cwnd_halve, coef_router_dropped)

#final_output=dat_exp.agg({'port': ['count'], 'bitrate': ['sum'], 'data_seg': ['sum'], 'retrans_ss': ['sum'], 'retrans_iperf': ['sum'], 'cwnd_halve': ['sum'], 'rtt': ['mean'] }) )
print( dat_exp.agg({'port': ['count'], 'bitrate': ['sum'], 'data_seg': ['sum'], 'retrans_ss': ['sum'], 'retrans_iperf': ['sum'], 'cwnd_halve': ['sum'], 'rtt': ['mean'] }) )


p=dat_exp['port'].aggregate('count')
bw=dat_exp['bitrate'].aggregate('sum')
seg=dat_exp['data_seg'].aggregate('sum')
retrans_ss_sum=dat_exp['retrans_ss'].aggregate('sum')
retrans_iperf_sum=dat_exp['retrans_iperf'].aggregate('sum')
cwn_halve_sum=dat_exp['cwnd_halve'].aggregate('sum')
rtt_mean=dat_exp['rtt'].aggregate('mean')


output_filename='/local/repository/cloudlab-scripts/output_mathis_C.csv'
if not os.path.isfile(output_filename):
    with open(output_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'time_duration', 'ports', 'Base_RTT(ms)', 'BW', 'total_data_seg_out','total_cwnd_half', 'total_retransmission_ss',\
        'total_retransmission_iperf', 'total_retransmission_ss/total_cwnd_half', 'total_retransmission_iperf/total_cwnd_half',\
        'C_ss', 'C_iperf', 'C_cwnd', 'C_router', 'router_dropped', 'router_sent', 'router_dropped/total_cwnd_half', \
        'mdape_ss', 'mdape_iperf', 'mdape_cwnd', 'mdape_router'
      writer.writerow(header)
      


x_retrans_ss=( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_ss_retrans'].values) ) ).values.reshape(-1,1)
x_retrans_iperf=( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_iperf_retrans'].values) ) ).values.reshape(-1,1)
x_cwnd=( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_cwnd_halve'].values) ) ).values.reshape(-1,1)
x_router=( (1448*8*1000)/(dat_exp['rtt']*np.sqrt(dat_exp['p_router_drop'].values) ) ).values.reshape(-1,1)
predicted_bw_ss    = LinearRegression(fit_intercept = False).fit(
  x_retrans_ss, 
  dat_exp['bitrate']*1000.0
).predict(x_retrans_ss)
predicted_bw_iperf = LinearRegression(fit_intercept = False).fit(
  x_retrans_iperf, 
  dat_exp['bitrate']*1000.0
).predict(x_retrans_iperf)
predicted_bw_cwnd    = LinearRegression(fit_intercept = False).fit(
  x_cwnd, 
  dat_exp['bitrate']*1000.0
).predict(x_cwnd)
predicted_bw_router = LinearRegression(fit_intercept = False).fit(
  x_router, 
  dat_exp['bitrate']*1000.0
).predict(x_router)

mdape_ss=np.median((np.abs(np.subtract(dat_exp['bitrate']*1000.0, predicted_bw_ss)/ (dat_exp['bitrate']*1000.0)))) * 100
mdape_iperf=np.median((np.abs(np.subtract(dat_exp['bitrate']*1000.0, predicted_bw_iperf)/ (dat_exp['bitrate']*1000.0)))) * 100
mdape_cwnd=np.median((np.abs(np.subtract(dat_exp['bitrate']*1000.0, predicted_bw_cwnd)/ (dat_exp['bitrate']*1000.0)))) * 100
mdape_router=np.median((np.abs(np.subtract(dat_exp['bitrate']*1000.0, predicted_bw_router)/ (dat_exp['bitrate']*1000.0)))) * 100

with open(output_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)   
  columns = duration, p, rtt, bw, seg, cwn_halve_sum, retrans_ss_sum,retrans_iperf_sum, retrans_ss_sum/cwn_halve_sum,\
    retrans_iperf_sum/cwn_halve_sum, coef_retrans_ss[0], coef_retrans_iperf[0], coef_cwnd_halve[0], coef_router_dropped[0],\
    n_seg_dropped, n_seg_sent, n_seg_dropped/cwn_halve_sum, mdape_ss, mdape_iperf,  mdape_cwnd, mdape_router
  writer.writerow(columns)

with PdfPages("linear_reg_plot.pdf") as pdf:
  plt.rcParams['figure.figsize'] = (8,6)

  plt.scatter(x=x_retrans_ss, y=dat_exp['bitrate']*1000.0, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x_retrans_ss, y=predicted_bw_ss, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x_retrans_ss, predicted_bw_ss, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)") 
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-1 calculation of packet_loss rate using data_seg_out from ss and retrans from ss data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x_retrans_iperf, y=dat_exp['bitrate']*1000.0, color='C4', s=10, label='actual values')
  plt.scatter(x=x_retrans_iperf, y=predicted_bw_iperf, color='C3', s=10, label='predicted_values')
  plt.plot(x_retrans_iperf, predicted_bw_iperf, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)") 
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-2: calculation of packet_loss rate using data_seg_out from ss and retrans from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()


  plt.scatter(x=x_cwnd, y=dat_exp['bitrate']*1000.0, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x_cwnd, y=predicted_bw_cwnd, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x_cwnd, predicted_bw_cwnd, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-3: calculation of packet_loss rate using data_seg_out from ss and cwnd from iperf3 data")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

  plt.scatter(x=x_router, y=dat_exp['bitrate']*1000.0, color='C4', alpha=1, s=10, label='actual values')
  plt.scatter(x=x_router, y=predicted_bw_router, color='C3',  alpha=1, s=10, label='predicted_values')
  plt.plot(x_router, predicted_bw_router, color='C2', linewidth=0.5, label='fit')
  plt.xlabel("x=mss/rtt*sqrt(packet_loss_rate)")
  plt.ylabel("y=bandwidth(bits/sec)")
  plt.title("Method-4: calculation of packet_loss rate using packet drop rate at the router")
  plt.legend()
  pdf.savefig()  # saves the current figure into a pdf page
  plt.show()
  plt.close()

