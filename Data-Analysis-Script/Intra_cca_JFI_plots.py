import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


N = 3
ind = np.arange(N) 
width = 0.25

dict_scale={'Edge':[0,50],'Intermediate':[90,500],'Core':[950,5000]}
dict_flows={'Edge':[10,30,50],'Intermediate':[100,300,500],'Core':[1000,3000,5000]}
rtt=[20,100,200]

#change the filename, default filename in which the data is stored is "jfi.csv"
filename="JFI_CloudLab.csv"
jfi_dat = pd.read_csv("JFI_CloudLab.csv", header=0, names=['cca', 'duration','rtt','BW','sq_BW', 'flow_count', 'jfi'])
cca=pd.unique(jfi_dat.cca)
flows=pd.unique(jfi_dat.flow_count)

with PdfPages("JFI_plot.pdf") as pdf:
  for i,c in enumerate(cca):
    for key in dict_scale:
        plt.rcParams['figure.figsize'] = (5,3)
        plt.rcParams['axes.axisbelow'] = True
        plt.grid(axis='y')
        dat_cca=jfi_dat[(jfi_dat['cca'] == c)]
        dat_cca.sort_values(by=['flow_count'])
        xvals = dat_cca.jfi[(dict_scale[key][0] <= jfi_dat['flow_count']) & (jfi_dat['flow_count'] <= dict_scale[key][1]) & (jfi_dat['rtt']==20)]
        print(xvals)     
        bar1 = plt.bar(ind, xvals, width, color = 'royalblue')
        yvals = dat_cca.jfi[(dict_scale[key][0] <= jfi_dat['flow_count']) & (jfi_dat['flow_count'] <= dict_scale[key][1]) & (jfi_dat['rtt']==100)]
        bar2 = plt.bar(ind+width+0.02, yvals, width, color='tomato')  
        zvals = dat_cca.jfi[(dict_scale[key][0] <= jfi_dat['flow_count']) & (jfi_dat['flow_count'] <= dict_scale[key][1]) & (jfi_dat['rtt']==200)]
        bar3 = plt.bar(ind+(width+0.02)*2, zvals, width, color = 'mediumspringgreen')
        plt.xlabel("Flow Count")
        plt.ylabel('JFI')
        plt.title(key+"Scale, "+"CCA-"+c)        
        plt.xticks(ind+width,dict_flows[key])
        plt.legend( (bar1,bar2, bar3), ('20ms', '100ms', '200ms'), bbox_to_anchor=(1, 0.5), frameon=False )   
        pdf.savefig(bbox_inches="tight")
        plt.show()
        plt.close()
