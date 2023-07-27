import csv
import re
import os
import sys


base_port=60000

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])
ip=sys.argv[1]
num_clients=int(sys.argv[2])
test_duration=int(sys.argv[3])
cca1=sys.argv[4]
flows=int(sys.argv[5])

id_dict={}
iperf_filename = "data-iperf-10.10.2.1"+ip+".csv"
cwn_filename= "data-cwn-10.10.2.1"+ip+".csv"
if not os.path.isfile(iperf_filename):
  with open(iperf_filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = 'socket', 'port', 'time', 'time_unit', 'transfer', 'transfer_unit', 'bitrate', 'bitrate_unit', 'retrans'
    writer.writerow(header)
   

if not os.path.isfile(cwn_filename):
  with open(cwn_filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = 'socket', 'port', 'cwnd'
    writer.writerow(header)


for j in range(1,num_clients+1):
   # print("sender-10.10.2.1"+ip+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt")
  with open("sender-10.10.2.1"+ip+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt", 'r') as file:
    lines = file.readlines()
  if '[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd\n' in lines:
    end_index1 = lines.index('[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd\n')
    #print(end_index1)
  elif '[ ID] Interval           Transfer     Bitrate         Retr  Cwnd\n' in lines:
    end_index1 = lines.index('[ ID] Interval           Transfer     Bitrate         Retr  Cwnd\n')       
  else:
    continue
  if '[ ID] Interval           Transfer     Bandwidth       Retr\n' in lines:
    end_index2 = lines.index('[ ID] Interval           Transfer     Bandwidth       Retr\n')
    #print(end_index2)
  elif '[ ID] Interval           Transfer     Bitrate         Retr\n' in lines:
    end_index2 = lines.index('[ ID] Interval           Transfer     Bitrate         Retr\n') 
  else:
    continue
  csv_lines = []
  data1 = [line.strip() for line in lines[1:end_index1]]
  if flows==1:
    data2= [line.strip() for line in lines[end_index2+1:-2]]
  else:
    data2= [line.strip() for line in lines[end_index2+1:-4]]
  lines2 = data2[::2]
 
    
  with open(iperf_filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for k in range(0,len(data1)):
        data1[k]=re.sub(r'\s+|\[', ' ', data1[k])
        words1 = data1[k].split()
        lines2[k]=re.sub(r'\s+|\[', ' ', lines2[k])
        words2 = lines2[k].split()
        id_dict[words1[0][:-1]]=words1[4]+words1[9]
        columns = words1[0][:-1], words1[4]+words1[9], words2[1], words2[2], words2[3], words2[4], words2[5], words2[6], words2[7]
        writer.writerow(columns)
    
    data_cwn=[line.strip() for line in lines[end_index1:end_index2]]
    with open(cwn_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for m in range(0,len(data_cwn)):
              data_cwn[m]=re.sub(r'\s+|\[', ' ', data_cwn[m])
              words_cwn = data_cwn[m].split()
              if words_cwn[0][:-1].isnumeric():
                if words_cwn[9]=='KBytes':
                  col=words_cwn[0][:-1], id_dict[words_cwn[0][:-1]], words_cwn[8]
                else:
                  col=words_cwn[0][:-1], id_dict[words_cwn[0][:-1]], float(words_cwn[8])*1000
                writer.writerow(col)
