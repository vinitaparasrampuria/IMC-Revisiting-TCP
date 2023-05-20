ip=$1
shift
declare -A cwnd_dict
declare -A halving_dict
declare -i ss_count
ss_count=1
rm /local/repository/cloudlab-scripts/file.txt
sstxt=$(ss --no-header -ein dst $ip)
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

while [ ! -z "$(ss --no-header -ein dst $ip)"  ]
do
ss_count+=1
sstxt=$(ss --no-header -ein dst $ip)
while read line_first; read line_second
do  
        local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
        current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
        prev_cwnd=$((${cwnd_dict[$local_port]}))
	#echo $local_port current congestion window is $current_cwnd
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
  echo "key  : $i" >>cwnd_data.txt
  echo "value: ${cwnd_dict[$i]}" >> cwnd_data.txt
done

for i in "${!halving_dict[@]}"
do
  echo "key  : $i" >>cwnd_half.txt
  echo "value: ${halving_dict[$i]}" >> cwnd_half.txt
done
