#delay (in ms) to be added to each receiver
delay=$1
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

#empty the result folder
rm -f result/*

if [ $type == 1 ] || [ $type == 2 ];
then
   for i in {0..9}
   do
      # use netem to configure the base delay on the receiver
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-servers'
      # with appropriate arguments

      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i /bin/bash << EOF
      bash /local/repository/endpoint-scripts/set-delay.sh $delay
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $num_clients > /dev/null 2>&1 &
EOF
   done
 else
   for i in {0..8}
   do
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i /bin/bash << EOF
      bash /local/repository/endpoint-scripts/set-delay.sh $delay
      sudo killall iperf3
      bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $num_clients
EOF
   done
   sudo ssh -o StrictHostKeyChecking=no root@receiver-9 /bin/bash << EOF
   bash /local/repository/endpoint-scripts/set-delay.sh $delay
   sudo killall iperf3
   bash /local/repository/endpoint-scripts/iperf-parallel-servers.sh $((num_clients+1))
EOF

 fi

 if [ $type == 1 ]
 then
   for i in {0..9}
   do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i  "bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
   done
  elif [ $type == 2 ]
  then
   for i in {0..4}
   do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i "bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
   done
   for i in {5..9}
   do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i "bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca2 $flows"
   done
  else
    for i in {0..8}
    do
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i "bash /local/repository/endpoint-scripts/iperf-parallel-senders.sh 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
     done
      sudo ssh -o StrictHostKeyChecking=no root@sender-9 "bash /local/repository/endpoint-scripts/iperf-parallel-senders-unequal.sh 10.10.2.19 $num_clients $test_duration $cca1 $flows $cca2"
  fi

 # sleep $((test_duration+60))

# do something here to analyze results and compute whatever you need

for i in {0..9}
do
sudo scp -o StrictHostKeyChecking=no -r root@sender-$i:./sender* /local/repository/cloudlab-scripts/result/.
done

if [ $type == 1 ]; then
jfi=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" .|awk '{sum+=$7}END {print sum}')
square=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" .|awk '{sum+=$7*$7}END {print sum}')
echo $square
count=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" .|awk '{count+=1}END {print count}')
echo count of $cca1 flows is $count
echo JFI is $jfi

else
sum1=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" result/*${cca1}.txt |awk '{sum+=$7} END {print sum}')
count1=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" result/*${cca1}.txt|awk '{count+=1}END {print count}')
echo count of flows of $cca1 is $count1
echo sum of Bandwidth of $cca1 is $sum1 Kbits/sec

sum2=$(grep -r -E "[0-9].*0.00-${test_duration}.*sender" result/*${cca2}.txt |awk '{sum+=$7} END {print sum}')
count2=$(grep -r -E "[0-9].*0.00-$test_duration.*sender" result/*${cca2}.txt|awk '{count+=1}END {print count}')
echo count of flows of $cca2 is $count2
echo sum of Bandwidth of $cca2 is $sum2 Kbits/sec
fi

for i in {0..9}
do

sudo ssh -o StrictHostKeyChecking=no root@receiver-$i "rm -f ./*"
sudo ssh -o StrictHostKeyChecking=no root@sender-$i "rm -f ./*"
done
