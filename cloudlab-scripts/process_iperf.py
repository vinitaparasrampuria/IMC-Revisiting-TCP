import csv
import re
#senders=10
#num_clients=10
#test_duration=7200
#cca1="reno"
base_port=60000

import sys

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
senders=int(sys.argv[1])
num_clients=int(sys.argv[2])
test_duration=int(sys.argv[3])
cca1=sys.argv[4]


for i in range(0,senders):
  csv_filename = 'output-10.10.2.1'+str(i)+'.csv'
  for j in range(1,num_clients+1):
   # print("sender-10.10.2.1"+str(i)+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt")
    with open("/local/repository/cloudlab-scripts/result-reno/sender-10.10.2.1"+str(i)+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt", 'r') as file:
        lines = file.readlines()

    # Find the indices of the first and last instance of [ID]
    end_index1 = lines.index('[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd\n')
    #print(end_index1)

    #last_index = len(lines) - lines[::-1].index('[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd\n') - 1
    end_index2 = lines.index('[ ID] Interval           Transfer     Bandwidth       Retr\n')
    #print(end_index2)
    csv_lines = []
    data1 = [line.strip() for line in lines[1:end_index1]]
    data2= [line.strip() for line in lines[end_index2+1:-4]]
    lines = data2[::2]
    #print(data1)
    #print(lines)
    #print(len(data1))
    #print(len(lines))
    


    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for k in range(0,len(data1)):
          data1[k]=re.sub(r'\s+', ' ', data1[k])
          words1 = data1[k].split()
          lines[k]=re.sub(r'\s+', ' ', lines[k])
          words2 = lines[k].split()
          
          columns = words1[1][:-1], words1[5]+words1[10], words2[2], words2[3], words2[4], words2[5], words2[6], words2[7], words2[8]
          writer.writerow(columns)
