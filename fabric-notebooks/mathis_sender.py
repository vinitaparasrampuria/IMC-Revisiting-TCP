import pandas as pd
import numpy as np
import csv
import sys
import os

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])    
i=int(sys.argv[1])


dat_exp = pd.DataFrame( columns=['port',
                           'data_seg',
                           'retrans_ss',
                           'rtt',
                           'bitrate',
                           'retrans_iperf']
 )


dat_ss = pd.read_csv("data-cwn-10.10.2.1"+str(i)+"-file.txt", header=None, names=['port', 'cwnd','rtt','data_seg','retrans'])
dat_cwn_iperf = pd.read_csv("data-cwn-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port','cwnd'])
dat_retrans_iperf= pd.read_csv("data-iperf-10.10.2.1"+str(i)+".csv",header=0, names=['socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'] )

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
#dat_exp = dat_exp.assign(p_router_drop = n_seg_dropped/n_seg_sent )


output_filename="packet_loss"+str(i)+".csv"
dat_exp.to_csv(output_filename, sep=',', index=False, encoding='utf-8')




