import re
import itertools
import os
import csv
import sys

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])	
ip=sys.argv[1]

output_filename="data-cwn-10.10.2.1"+ip+"-file.txt"

with open("sender-cwn1-10.10.2.1"+ip+"-file.txt", 'r') as file:
    for line1,line2 in itertools.zip_longest(*[file]*2):
       
      ip1_match = re.search(r"10\.10\.1\.1"+ip+":([\d]+)", line1)
      if ip1_match:
          value_after_ip1 = int(ip1_match.group(1))
          #print(f"Value after 10.10.1.10: {value_after_ip1}")

      ip2_match = re.search(r"10\.10\.2\.1"+ip+":([\d]+)", line1)
      if ip2_match:
          value_after_ip2 = int(ip2_match.group(1))
          #print(f"Value after 10.10.2.10: {value_after_ip2}") 

      cwnd_match = re.search(r"cwnd:(\d+)", line2)
      if cwnd_match:
          cwnd = int(cwnd_match.group(1))
          print(f"cwnd value: {cwnd}")
      
      rtt_match = re.search(r"rtt:(\d+)", line2)
      if rtt_match:
          rtt = int(rtt_match.group(1))
          print(f"rtt value: {rtt}")
      else:
        rtt=None

      with open(output_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        columns = ip1_match.group(1)+ip2_match.group(1), cwnd , rtt
        writer.writerow(columns)
