#delay (in ms) to be added to each receiver
delay=$1
shift

#set limit for tc qdisc on esch receiver (10000, 100000 etc)
limit=$1
shift

#type of test
#1 for intra CCA
#2 for inter cca- equal flows divided between two cca
#3 for inter cca- unequal flows divided between two cca
#like bbr-1 and reno 1000
type=$1
shift

# E.g. 5
num_clients=$1
shift

# E.g. 60
test_duration=$1
shift

#CCA-bbr, cubic, reno
cca1=$1
shift

#number of flows to be sent from one iperf3
flows=$1
shift

#CCA-bbr, cubic, reno for inter flow
cca2=$1
shift

#get queue statistics before running the experiment
router_egress_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" )
tc -p -s -d -j qdisc show dev $router_egress_name >tc_before.txt

if [ $type == 1 ] || [ $type == 2 ];
then
   for i in {0..9}
   do
      # run 'bash /local/repository/endpoint-scripts/set-delay.sh $delay' to add delay on the receiver
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-servers'
      # with appropriate arguments

      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i /bin/bash << EOF
      bash /local/repository/endpoint-scripts/set-delay.sh $delay $limit
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $num_clients > /dev/null 2>&1 &
EOF
   done
 else
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
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows
EOF
   done
  elif [ $type == 2 ];
  then
   #empty the result folder
   rm -f result-${cca1}-${cca2}/*
   rmdir result-${cca1}-${cca2}*
   #make a new directory to store the results
   mkdir /local/repository/cloudlab-scripts/result-${cca1}-${cca2}
   for i in {0..4}
   do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows
EOF
   done
   for i in {5..9}
   do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca2 $flows
EOF
   done
  else
   #empty the result folder
   rm -f result-${cca1}-${cca2}/*
   rmdir result-${cca1}-${cca2}*
   #make a new directory to store the results
   mkdir /local/repository/cloudlab-scripts/result-${cca1}-${cca2}
    for i in {0..8}
    do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i /bin/bash << EOF
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows
EOF
     done
      sudo ssh -o StrictHostKeyChecking=no root@sender-9 /bin/bash << EOF
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-senders-unequal.sh 10.10.2.19 $num_clients $test_duration $cca1 $flows $cca2
EOF
  fi

sleep $((test_duration+300))

#get queue statistics after running the experiment
tc -p -s -d -j qdisc show dev $router_egress_name >tc_after.txt

# analyze results

if [ $type == 1 ]; then
   for i in {0..9}
   do
   sudo scp -o StrictHostKeyChecking=no -r root@sender-$i:./sender* /local/repository/cloudlab-scripts/result-${cca1}/.
   done
else
   for i in {0..9}
   do
   sudo scp -o StrictHostKeyChecking=no -r root@sender-$i:./sender* /local/repository/cloudlab-scripts/result-${cca1}-${cca2}/.
   done
fi

if [ $type == 1 ]; then
jfi=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1} |awk '{sum+=$7}{sq+=$7*$7}{count+=1} END {print (sum*sum)/(sq*count)}')
sum=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1} |awk '{sum+=$7}END {print sum}')
echo sum of bandwidth is $sum Kbits/sec
square=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1} |awk '{sum+=$7*$7}END {print sum}')
echo square is $square
count=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1} |awk '{count+=1}END {print count}')
echo count of $cca1 flows is $count
echo JFI is $jfi

else
sum1=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1}-${cca2} |awk '{sum+=$7} END {print sum}')
count1=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" --include *${cca1}.txt /local/repository/cloudlab-scripts/result-${cca1}-${cca2}|awk '{count+=1}END {print count}')
echo count of flows of $cca1 is $count1
echo sum of Bandwidth of $cca1 is $sum1 Kbits/sec

sum2=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" --include *${cca2}.txt /local/repository/cloudlab-scripts/result-${cca1}-${cca2} |awk '{sum+=$7} END {print sum}')
count2=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" --include *${cca2}.txt /local/repository/cloudlab-scripts/result-${cca1}-${cca2}|awk '{count+=1}END {print count}')
echo count of flows of $cca2 is $count2
echo sum of Bandwidth of $cca2 is $sum2 Kbits/sec
fi

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


for i in {0..9}
do

sudo ssh -o StrictHostKeyChecking=no root@receiver-$i "rm -f ./*"
sudo ssh -o StrictHostKeyChecking=no root@sender-$i "rm -f ./*"
done
