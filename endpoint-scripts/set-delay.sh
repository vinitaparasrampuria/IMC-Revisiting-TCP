#delay to be added
delay=$1
shift

limit=$1
shift

receiver_inf_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" );
sudo tc qdisc del dev $receiver_inf_name root netem
sudo tc qdisc add dev $receiver_inf_name root netem delay ${delay}ms limit ${limit}

tc -s -d qdisc show dev $receiver_inf_name
