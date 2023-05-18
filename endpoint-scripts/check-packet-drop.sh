
receiver_inf_name=$( ip route get 10.10.2.100 | grep -oP "(?<=dev )[^ ]+" );

tc -s -d qdisc show dev $receiver_inf_name
