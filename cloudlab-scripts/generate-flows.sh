# delay (in ms) to be added to each receiver (for this expt values are 20, 100 and 200 ms)
delay=$1

# set limit for tc qdisc on esch receiver (10000, 100000 etc)
limit=$2

# type of test
# 1 for intra CCA and Mathis constant Calculation
# 2 for inter cca- equal flows divided between two cca
# 3 for inter cca- unequal flows divided between two cca
# like bbr-1 and reno 999
type=$3

# E.g. 10
# For this expt, the value is 10 for core scale and 1 for edge scale
num_clients=$4

# E.g. 1800
# For this experiment, this value is 10800 (=3 hours)
test_duration=$5

# CCA1-bbr, cubic, reno
# To get Mathis constant this is set to reno
# To get intra and inter CCA fairness, it can be bbr, cubic, reno

cca1=$6

# number of flows to be sent from one iperf3
# For this expt, core scale, this is set to 10, 30 and 50 (to get 1000, 3000 and 5000 flows)
# edge scale, 1, 3 and 5 (to get 10, 30 and 50 flows)
flows=$7

# interval(in sec) in which iperf3 data is saved
# for getting Mathos constant this is set to 0.01
# for all other expts, this value is set to 1
interval=$8

#time (in sec) to omit the initial iperf3 results
omit=$9

# CCA2-bbr, cubic, reno 
# This is used only in inter flow fairness expts
cca2=${10}

# remove existing files from all the hosts
for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@receiver-$i "rm -f ./*"
   sudo ssh -o StrictHostKeyChecking=no root@sender-$i "rm -f ./*"
done

# get queue statistics at the router before running the experiment
router_egress_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" )
tc -p -s -d -j qdisc show dev $router_egress_name >tc_before.txt

if [ $type == 1 ] || [ $type == 2 ];
then
   for i in {0..9}
   do
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i /bin/bash << EOF
      bash /local/repository/endpoint-scripts/set-delay.sh $delay $limit
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $num_clients > /dev/null 2>&1 &
EOF
   done
elif [ $type == 3 ];
then
   for i in {0..8}
   do
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i /bin/bash << EOF
      bash /local/repository/endpoint-scripts/set-delay.sh $delay $limit
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $num_clients
EOF
   done
   sudo ssh -o StrictHostKeyChecking=no root@receiver-9 /bin/bash << EOF
   bash /local/repository/endpoint-scripts/set-delay.sh $delay $limit
   sudo killall iperf3
   bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $((num_clients+1))
EOF
else
   echo "Wrong input"
fi

if [ $type == 1 ];
then
   #empty the result folder
   rm -f result-${cca1}/*
   rmdir result-${cca1}*
   #make a new directory to store the results
   mkdir /local/repository/cloudlab-scripts/result-${cca1}
   for i in {0..9}
   do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
      rm -f /mydata/*
      cd /mydata
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows $interval $omit > /dev/null 2>&1 &
EOF
   done
 elif [ $type == 2 ];
 then
      #empty the result folder
      rm -f /mydata/result-${cca1}-${cca2}/*
      rmdir /mydata/result-${cca1}-${cca2}*
      #make a new directory to store the results
      mkdir /mydata/result-${cca1}-${cca2}
      for i in {0..4}
      do
         sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
         rm -f /mydata/*
         cd /mydata
         sudo killall iperf3
         bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows $interval $omit > /dev/null 2>&1 &
EOF
   done
      for i in {5..9}
      do
         sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
         rm -f /mydata/*
         cd /mydata
         sudo killall iperf3
         bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca2 $flows $interval $omit > /dev/null 2>&1 &
EOF
   done
 elif [ $type == 3 ];
 then
      #empty the result folder
      rm -f /mydata/result-${cca1}-${cca2}/*
      rmdir mydata/result-${cca1}-${cca2}*
      #make a new directory to store the results
      mkdir /mydata/result-${cca1}-${cca2}
      for i in {0..8}
      do
         sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
         rm -f /mydata/*
         cd /mydata
         sudo killall iperf3
         bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows $interval $omit > /dev/null 2>&1 &
EOF
       done
         sudo ssh -o StrictHostKeyChecking=no root@sender-9 /bin/bash << EOF
         rm -f /mydata/*
         cd /mydata
         sudo killall iperf3
         bash /local/repository/endpoint-scripts/iperf-parallel-senders-unequal.sh 10.10.2.19 $num_clients $test_duration $cca1 $flows $cca2 $interval $omit > /dev/null 2>&1 &
EOF
else
   echo "Wrong input"
fi

sleep $((test_duration+300))

for i in {0..9}
do
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i "bash /local/repository/endpoint-scripts/check-packet-drop.sh"
done

#get queue statistics after running the experiment
tc -p -s -d -j qdisc show dev $router_egress_name >tc_after.txt

# analyze results

#To get packet dropped:
drop_before=$(cat tc_before.txt| grep -m 1 '"drops":' | awk '{print $2}' |cut -d ',' -f1)

#To get packets sent
sent_before=$(cat tc_before.txt| grep -m 1 '"packets":' | awk '{print $2}' |cut -d ',' -f1)

#To get packet dropped:
drop_after=$(cat tc_after.txt| grep -m 1 '"drops":' | awk '{print $2}' |cut -d ',' -f1)

#To get packets sent
sent_after=$(cat tc_after.txt| grep -m 1 '"packets":' | awk '{print $2}' |cut -d ',' -f1)

#Calculate packet drop rate:

dropped=$(($drop_after-$drop_before))
sent=$(($sent_after-$sent_before))
drop_rate=$(echo "scale=8;$dropped/$sent" | bc)

echo packet drop before running experiment
echo $drop_before
echo packet sent before running experiment
echo $sent_before
echo packet drop after running experiment
echo $drop_after
echo packet sent after  running experiment
echo $sent_after
echo packet drop rate
echo $drop_rate

sleep 60

if [ $type == 1 ]; then
   for i in {0..9}
   do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
      cd /mydata
      if [ $cca1 == 'reno' ]; then
      python3 /local/repository/endpoint-scripts/process_cwn_file.py $i > /dev/null 2>&1 &
      fi
      python3 /local/repository/endpoint-scripts/process_iperf_normal.py $i $num_clients $test_duration $cca1 $flows > /dev/null 2>&1 &
EOF
   done
   while [ True ]; 
   do 
      sleep 120
      j=False
      for i in {0..9} 
      do 
         res=$(sudo ssh -o StrictHostKeyChecking=no root@sender-$i  pgrep -af python) 
      if [[ $res == *"process"* ]]; 
      then 
         j=True
      fi
      done
   if [[ $j == True ]];
      then continue 
   else 
      break
   fi
   done
   
   for i in {0..9}
   do
      sudo scp -o StrictHostKeyChecking=no -r root@sender-$i:/mydata/data* /local/repository/cloudlab-scripts/result-${cca1}/.
   done
elif [ $type == 2 ] || [ $type == 3 ]; then
   for i in {0..9}
   do
      sudo scp -o StrictHostKeyChecking=no -r root@sender-$i:/mydata/sender* /mydata/result-${cca1}-${cca2}/.
   done
else
   echo "Wrong input"
fi

if [ $type == 1 ]; then
   python3 /local/repository/cloudlab-scripts/get_JFI.py 10 $num_clients $cca1 $test_duration $delay
   if [ $cca1 == 'reno' ]; then
      python3 /local/repository/cloudlab-scripts/mathis_constant_cal.py 10 $num_clients $cca1 $dropped $sent $test_duration $delay
   fi
  
elif [ $type == 2 ] || [ $type == 3 ];
then
   cd /mydata
   sum_cca1=$(grep -r -E "[0-9].*0.00-[0-9].*sender" --include *${cca1}.txt /mydata/result-${cca1}-${cca2} |tr '[' ' ' |awk -F ' ' '{sum+=$7} END {print sum}')
   count1=$(grep -r -E "[0-9].*0.00-[0-9].*sender" --include *${cca1}.txt /mydata/result-${cca1}-${cca2} |tr '[' ' ' |awk -F ' ' '{count+=1}END {print count}')
   echo count of flows of $cca1 is $count1
   echo sum of Bandwidth of $cca1 is $sum_cca1 Kbits/sec

   sum_cca2=$(grep -r -E "[0-9].*0.00-[0-9].*sender" --include *${cca2}.txt /mydata/result-${cca1}-${cca2} |tr '[' ' ' |awk -F ' ' '{sum+=$7} END {print sum}')
   count2=$(grep -r -E "[0-9].*0.00-[0-9].*sender" --include *${cca2}.txt /mydata/result-${cca1}-${cca2} |tr '[' ' ' |awk -F ' ' '{count+=1}END {print count}')
   echo count of flows of $cca2 is $count2
   echo sum of Bandwidth of $cca2 is $sum_cca2 Kbits/sec
   total_bandwidth=$((sum_cca1+sum_cca2))
   tput_ratio=$(echo "scale=4; $sum_cca1/$total_bandwidth" | bc)
   tout_percent=$(echo "scale=4; $tput_ratio*100" | bc)
   tput_filename=/local/repository/cloudlab-scripts/inter-cca-tput.csv
   if test -f "$tput_filename"; then
      echo $cca1, $cca2, $total_bandwidth, $delay, $sum_cca1, $count1, $sum_cca2, $count2, $tout_percent  >> $tput_filename
   else
      echo "CCA1,CCA2,Total Bandwidth(Kbps),Base RTT(ms),Sum of CCA1,CCA1 Flow Count,Sum of CCA2,CCA2 Flow Count,Throughput%" >> $tput_filename;
      echo $cca1, $cca2, $total_bandwidth, $delay, $sum_cca1, $count1, $sum_cca2, $count2, $tout_percent  >> $tput_filename
   fi
   cd /local/repository/cloudlab-scripts/
else
   echo "Wrong input"
fi

