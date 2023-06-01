
sender_inf_name=$( ip route get 10.10.1.100 | grep -oP "(?<=dev )[^ ]+" );
sudo tc qdisc replace dev $sender_inf_name root handle 1: pfifo_fast
tc -s -d qdisc show dev $sender_inf_name
