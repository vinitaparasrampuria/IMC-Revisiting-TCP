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


if [$type -eq 1] || [$type -eq 2] 
then
   for i in {0..9}
   do
      # use netem to configure the base delay on the receiver
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-servers'
      # with appropriate arguments
      
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i 
      'receiver_inf_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" );
      sudo tc qdisc add dev $receiver_inf_name root netem delay $delay;
      bash /local/repository/endpoint-scripts/iperf-parallel-servers $num_clients'
   done
 else
   for i in {0..8}
   do
      # use netem to configure the base delay on the receiver
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-servers'
      # with appropriate arguments
      
      sudo ssh -o StrictHostKeyChecking=no root@receiver-$i 
      'receiver_inf_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" );
      echo receiver_inf_name;
      sudo tc qdisc add dev $receiver_inf_name root netem delay $delay;
      bash /local/repository/endpoint-scripts/iperf-parallel-servers $num_clients'
   done
   sudo ssh -o StrictHostKeyChecking=no root@receiver-9
   'receiver_inf_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" );
   sudo tc qdisc add dev $receiver_inf_name root netem delay $delay;
   bash /local/repository/endpoint-scripts/iperf-parallel-servers $((num_clients+1))'
   
 fi
 
 if [$type -eq 1]
 then
   for i in {0..9}
   do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i 
      "bash /local/repository/endpoint-scripts/iperf-parallel-senders 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
   done
  elif [$type -eq 2]
  then
   for i in {0..4}
   do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i 
      "bash /local/repository/endpoint-scripts/iperf-parallel-senders 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
   done
   for i in {5..9}
   do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i 
      "bash /local/repository/endpoint-scripts/iperf-parallel-senders 10.10.2.1$i $num_clients $test_duration $cca2 $flows"
   done
  else
    for i in {0..8}
    do
      # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
      # with appropriate arguments
      sudo ssh -o StrictHostKeyChecking=no root@sender-$i 
      "bash /local/repository/endpoint-scripts/iperf-parallel-senders 10.10.2.1$i $num_clients $test_duration $cca1 $flows"
     done
      sudo ssh -o StrictHostKeyChecking=no root@sender-9 
      "bash /local/repository/endpoint-scripts/iperf-parallel-senders_unequal 10.10.2.19 $num_clients $test_duration $cca1 $flows $cca2"   
  fi

sleep $test_duration+300

# do something here to analyze results and compute whatever you need

