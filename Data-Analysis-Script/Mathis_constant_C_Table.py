pip install pdfkit
pip install reportlab

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import pandas as pd

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

for r in rtt:  
    for key in dict_scale:
        if key=='Edge':
          continue
        xvals = dat[(dict_scale[key][0] <= dat['ports']) & (dat['ports'] <= dict_scale[key][1]) & (dat['base_rtt']==r)]  
        xvals=xvals.sort_values(by=['ports'])

        xvals_edge = dat[(dict_scale['Edge'][0] <= dat['ports']) & (dat['ports'] <= dict_scale['Edge'][1]) & (dat['base_rtt']==r)]
        packet_loss_C= [xvals_edge['C_router'].aggregate('mean')]
        packet_loss=packet_loss_C+xvals['C_router'].values.tolist()
        print(packet_loss)
        CWND_half_C= [xvals_edge['C_cwnd'].aggregate('mean')]
        data = {  
        "Packet Loss": packet_loss_C+xvals['C_router'].values.tolist(),
        "CWND Halving": CWND_half_C+xvals['C_cwnd'].values.tolist()}
        df = pd.DataFrame(data)
        cols = df.columns.tolist()
        for prsn in range(0, df.shape[1]):
          df[cols[prsn]] = df[cols[prsn]].apply(lambda x: f'{"{:.2f}".format(float(x))}')
        df = df.T.reset_index()
        my_list = [['p('+str(r)+"ms)", 'EdgeScale', key+"Scale Flow Count"]]+ [["Flow"," "]+dict_flows[key]]+ df.values.tolist()
        table = Table(my_list)
        table.setStyle(TableStyle([('SPAN', (0, 0), (0, 1)),
                                   (('SPAN', (1, 0), (1, 1))),
                          ('SPAN', (2, 0), (-1, 0)),
                          ('BACKGROUND', (0,0), (-1,0), colors.white),
                          ('BACKGROUND',(0,1),(-1,-1),colors.white),
                          ('BACKGROUND', (0,0), (0,1), colors.white),
                          ('TEXTCOLOR',(0,0),(-1,0),colors.black),
                          ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                          ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
                          ('FONTSIZE', (0,0), (-1,0), 12),
                          ('BOTTOMPADDING', (0,0), (-1,0), 12),
                          ('LINEABOVE', (1, 2), (-1, 2), 1, colors.black),
                          ('GRID',(0, 0), (-1,-1),1,colors.black)]))
        pdf_file = key+str(r)+'ms.pdf'
        c = canvas.Canvas(pdf_file, pagesize=letter)
        table.wrapOn(c, inch*7, inch*2)
        table.drawOn(c, x=50, y=650)
        c.save()
