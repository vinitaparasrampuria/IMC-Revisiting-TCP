ip=$1
shift
declare -A cwnd_dict
declare -A halving_dict
declare -i ss_count
#declare -A total_ss_dict
ss_count=1

sstxt=$(ss --no-header -ein dst $ip)
while read line_first; read line_second
do
      
        local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
	current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
	cwnd_dict[$local_port]=$current_cwnd
	halving_dict[$local_port]=0
	#total_ss_dict[$local_port]=1
	echo "$local_port,$current_cwnd" >>sender-cwn-$ip-initial-file.txt
done <<< "$sstxt"

while [ 1 ]
do
ss_count=$((ss_count+1))

sstxt=$(ss --no-header -ein dst $ip)
if [ ! -z "$sstxt" ]; then
	while read line_first; read line_second
	do  
        local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
        current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
        prev_cwnd=$((${cwnd_dict[$local_port]}))
	#echo $local_port current congestion window is $current_cwnd
	echo prev_cwnd: $prev_cwnd
		if [ ! -v halving_dict[$local_port] ]; then
			halving_dict[$local_port]=0
		fi
		#if [ ! -v total_ss_dict[$local_port] ]; then
		#	total_ss_dict[$local_port]=1
		#else
		#	 ((total_ss_dict[$local_port]++))
		#fi
		if [[ ! -z "$prev_cwnd" ]] && [[ "$current_cwnd" -lt "$prev_cwnd" ]]; then
			((halving_dict[$local_port]++))
		fi
		cwnd_dict[$local_port]=$current_cwnd
		#echo "$local_port,$current_cwnd" >> sender-cwn-$ip-after-file.txt
		done <<< "$sstxt"
else
	break
fi
done
	echo  $ss_count >> sender-cwn-ss-count-$ip.txt

for i in "${!cwnd_dict[@]}"
do
  echo "$i,${cwnd_dict[$i]}" >> sender-cwn-dict-$ip.txt
done
declare -i count

for i in "${!halving_dict[@]}"
do
  echo "$i,${halving_dict[$i]}" >> sender-cwn-halving-dict-$ip.txt
	if [ ${halving_dict[$i]} -gt 0 ]; then
		count=$((count+1))
	fi
done
	echo $count >> sender-cwn-ss-count-$ip.txt
	echo $((count*ss_count)) >> sender-cwn-ss-count-$ip.txt


#for i in "${!total_ss_dict[@]}"
#do
#	echo "$i,${total_ss_dict[$i]}" >> sender-cwn-ss-dict-$ip.txt
#done
