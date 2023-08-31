
router_egress_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" )

sudo tc qdisc del dev $router_egress_name root
sudo tc qdisc add dev $router_egress_name root handle 1: htb default 3
sudo tc class add dev $router_egress_name parent 1: classid 1:3 htb rate 100Mbit
sudo tc qdisc add dev $router_egress_name parent 1:3 handle 3: bfifo limit 3M


echo "Capacity test with multiple flows"

for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@receiver-$i 'iperf3 -s -1 -f g -D --logfile validate.dat'
done

for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@sender-$i "nohup iperf3 -t 120 -c 10.10.2.1$i > /dev/null 2>&1 &"
done

sleep 245


for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@receiver-$i "tail --lines=2 validate.dat | grep receiver | awk '{print $6}'" 
done

echo "Capacity test with one flow"

sudo ssh -o StrictHostKeyChecking=no root@receiver-0 'iperf3 -s -1 -f g -D'
sudo ssh -o StrictHostKeyChecking=no root@sender-0  "iperf3 -t 60 -i 60 -c 10.10.2.10"


echo "Latency test"

for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@sender-$i "ping -c 5 10.10.2.1$i | grep rtt"
done

