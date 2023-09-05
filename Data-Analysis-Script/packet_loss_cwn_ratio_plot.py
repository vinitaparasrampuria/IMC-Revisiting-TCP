import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


dict_scale={'Edge':[0,50],'Intermediate':[90,500],'Core':[950,5000]}
dict_flows={'Edge':[10,30,50],'Intermediate':[100,300,500],'Core':[1000,3000,5000]}
rtt=[20,100,200]

#change the filename, default filename in which the data is stored is "output_mathis_C.csv"
filename="C_CloudLab.csv"
dat = pd.read_csv(filename, header=0, 
                      names=['time_duration', 'ports', 'base_rtt', 'BW', 'total_data_seg_out','total_cwnd_half', 'total_retransmission_ss',\
        'total_retransmission_iperf', 'total_retransmission_ss_to_total_cwnd_half', 'total_retransmission_iperf_to_total_cwnd_half',\
        'C_ss', 'C_iperf', 'C_cwnd', 'C_router', 'router_dropped', 'router_sent', 'router_dropped_to_total_cwnd_half', \
        'mdape_ss', 'mdape_iperf', 'mdape_cwnd', 'mdape_router'])


with PdfPages("Ratio_plot.pdf") as pdf:
  for r in rtt:
    for key in dict_scale: 
        plt.figure()
        plt.rcParams['figure.figsize'] = (5,2)
        plt.rcParams['axes.axisbelow'] = True
        plt.grid()
        xvals = dat[(dict_scale[key][0] <= dat['ports']) & (dat['ports'] <= dict_scale[key][1]) & (dat['base_rtt']==r)]   
        plt.plot(dict_flows[key],xvals.router_dropped_to_total_cwnd_half)  
        plt.xlabel("Flow Count")
        plt.ylabel('JFI')
        plt.title(key+"Scale at base RTT of "+str(r)+"ms")        
        plt.ylim(0,max(20,max(xvals.router_dropped_to_total_cwnd_half)+2.5))
        plt.yticks(np.arange(0,max(20,max(xvals.router_dropped_to_total_cwnd_half)+2.5),5))
        plt.xticks(dict_flows[key])
        pdf.savefig(bbox_inches="tight")
        plt.show()
        plt.close()
