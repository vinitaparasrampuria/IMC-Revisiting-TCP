erimport json
import csv
import os
import sys


for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
senders=int(sys.argv[1])
num_clients=int(sys.argv[2])
test_duration=int(sys.argv[3])
cca1=sys.argv[4]
base_port=60000



for i in range(0,senders):
  iperf_filename =  "/local/repository/cloudlab-scripts/result-"+cca1+"/data-iperf-10.10.2.1"+str(i)+".txt"
  cwn_filename = "/local/repository/cloudlab-scripts/result-"+cca1+"/data-cwn-10.10.2.1"+str(i)+".txt"
  if not os.path.isfile(iperf_filename):
    with open(iperf_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'socket', 'port', 'retransmits', 'send_rate', 'bytes_sent'
      writer.writerow(header)
   

  if not os.path.isfile(cwn_filename):
    with open(cwn_filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      header = 'socket', 'port', 'cwnd'
      writer.writerow(header)

  for j in range(1,num_clients+1):
    #print("/local/repository/cloudlab-scripts/result-"+cca1+"/sender-10.10.2.1"+str(i)+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt")
    f=open("/local/repository/cloudlab-scripts/result-"+cca1+"/sender-10.10.2.1"+str(i)+"-"+str(base_port+j)+"-"+str(test_duration)+"-"+cca1+".txt")
    data = json.load(f)
    socket_dict={}
    if not data:
        continue

    for k in range (0, len(data['start']['connected'])):
      socket=data['start']['connected'][k]['socket']
      port=str(data['start']['connected'][k]['local_port'])+str(data['start']['connected'][k]['remote_port'])
      print(socket)
      print(port)
      socket_dict[socket] = port

    for l in range(0,len(data['end']['streams'])):
      s=data['end']['streams'][l]['sender']['socket']
      bytes_sent=data['end']['streams'][l]['sender']['bytes']
      send_rate=data['end']['streams'][l]['sender']['bits_per_second']
      retransmits=data['end']['streams'][l]['sender']['retransmits']
      with open(iperf_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        columns = s, socket_dict[s], retransmits, send_rate, bytes_sent
        writer.writerow(columns)


    for m in range (0, len(data['intervals'])):
      for n in range (0, len(data['intervals'][m]['streams'])):
        s=data['intervals'][m]['streams'][n]['socket']
        cwnd=data['intervals'][m]['streams'][n]['snd_cwnd']
        rtt=data['intervals'][m]['streams'][n]['rtt']
        with open(cwn_filename, 'a', newline='') as csvfile:
          writer = csv.writer(csvfile)
          columns = s, socket_dict[s], cwnd, rtt
          writer.writerow(columns)

    f.close()
