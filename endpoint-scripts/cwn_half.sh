declare -A cwnd_dict
declare -A halving_dict
declare -i ss_count
ss_count=1
sstxt=$(ss --no-header -ein dst 10.10.2.10)
while read line_first; read line_second
do
        echo "New line";
        local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
	current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
        echo $local_port current congestion window is $current_cwnd
	cwnd_dict[$local_port]=$current_cwnd
	halving_dict[$local_port]=0
	echo "$local_port,$current_cwnd" >> file.txt
done <<< "$sstxt"

while [ ! -z "$(ss --no-header -ein dst 10.10.2.10)"  ]
do
ss_count+=1
sstxt=$(ss --no-header -ein dst 10.10.2.10)
while read line_first; read line_second
do 
        echo "New line"; 
        local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
        current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
        prev_cwnd=$((${cwnd_dict[$local_port]}))
	echo $local_port current congestion window is $current_cwnd
	echo $prev_cwnd
	if [[ ! -z "$prev_cwnd" ]] && [[ "$current_cwnd" -lt "$prev_cwnd" ]]; then
		curr_count= $((${halving_dict[$local_port]}+1))
		halving_dict[$local_port]=curr_count
	fi
	cwnd_dict[$local_port]=$current_cwnd
echo "$local_port,$current_cwnd" >> file.txt
done <<< "$sstxt"
done
echo  $ss_count

for i in "${!cwnd_dict[@]}"
do
  echo "key  : $i"
  echo "value: ${cwnd_dict[$i]}"
done

for i in "${!halving_dict[@]}"
do
  echo "key  : $i"
  echo "value: ${halving_dict[$i]}"
done
