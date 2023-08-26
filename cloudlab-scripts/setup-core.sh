
router_egress_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" )

sudo ethtool  -K $router_egress_name hw-tc-offload on
sudo ethtool  -k $router_egress_name | grep hw-tc-offload

sudo tc qdisc del dev $router_egress_name root
sudo tc qdisc replace dev $router_egress_name root handle 1: bfifo limit 375MB
sudo mlnx_qos -i $router_egress_name -p 0,0,0,0,0,0,0,0 -r 10,0,0,0,0,0,0,0

echo "Capacity test with multiple flows"

for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@receiver-$i 'iperf3 -s -1 -f g -D --logfile validate.dat'
done

for i in {0..9}
do
   sudo ssh -o StrictHostKeyChecking=no root@sender-$i "nohup iperf3 -t 120 -c 10.10.2.1$i > /dev/null 2>&1 &"
done

sleep 240


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


