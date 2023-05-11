


for i in {0..9}
do
   # use netem to configure the base delay on the receiver
   # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-servers'
   # with appropriate arguments
   sudo ssh -o StrictHostKeyChecking=no root@receiver-$i 'iperf3 -s -1 -f g -D --logfile validate.dat'
done

for i in {0..9}
do
   # instead of running iperf3 directly, run 'bash /local/repository/endpoint-scripts/iperf-parallel-senders'
   # with appropriate arguments
   sudo ssh -o StrictHostKeyChecking=no root@sender-$i "nohup iperf3 -t 60 -P 10 -c 10.10.2.1$i > /dev/null 2>&1 &"
done

sleep 65

# do something here to analyze results and compute whatever you need

