import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


N = 3
ind = np.arange(N)
width = 0.25
with PdfPages("MedianError_plot.pdf") as pdf:

  plt.rcParams['figure.figsize'] = (5,2)

  for r in rtt:
      for key in dict_scale:
        if key=='Edge':
          continue
        fig, ax1 = plt.subplots()
        ax1.set_axisbelow(True)
        ax1.grid()
        xvals = dat[(dict_scale[key][0] <= dat['ports']) & (dat['ports'] <= dict_scale[key][1]) & (dat['base_rtt']==r)]
        xvals=xvals.sort_values(by=['ports'])
        bar1 = ax1.bar(ind, xvals.mdape_router, width, color = 'chocolate')
        bar2 = ax1.bar(ind+width+0.02, xvals.mdape_cwnd, width, color = 'blue')
        ax1.set_xlabel("Flow Count")
        ax1.set_ylabel('Error (%)')
        ax1.set_title(key+"Scale at Base RTT of "+str(r)+"ms")
        ax1.set_xticks(ind+0.1, labels=dict_flows[key])
        ax1.legend( (bar1,bar2), ("Packet Loss Rate", "CWND Halving Rate"), loc='upper left', bbox_to_anchor=(1, 1), frameon=False )
        ax1.set_ylim(0,20)

        xvals_edge = dat[(dict_scale['Edge'][0] <= dat['ports']) & (dat['ports'] <= dict_scale['Edge'][1]) & (dat['base_rtt']==r)]
        xvals_edge=xvals_edge.sort_values(by=['ports'])
        ax2 = ax1.twiny()
        ax2.tick_params(top=False, right=False, labelright=False, labeltop=False, gridOn=False)
        ax3 = ax2.twinx()
        ax3.plot(dict_flows['Edge'],xvals_edge.mdape_router, color='red')
        ax3.set_ylim(0,20)
        ax3.legend( ["Home, Packet Loss"], bbox_to_anchor=(1, 0.3),  loc='upper left', frameon=False)
        ax3.tick_params(top=False, right=False, labelright=False, labeltop=False, gridOn=False)
        ax4 = ax2.twinx()
        ax4.plot(dict_flows['Edge'],xvals_edge.mdape_cwnd, color='cyan')
        ax4.set_ylim(0,20)
        ax4.legend( ["Home, CWND Halving"], bbox_to_anchor=(1, 0.2),  loc='upper left', frameon=False)
        ax4.tick_params(top=False, right=False, labelright=False, labeltop=False, gridOn=False)
        pdf.savefig(bbox_inches="tight")
        plt.show()
        plt.close()
