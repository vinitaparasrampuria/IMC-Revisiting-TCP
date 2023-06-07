ip=$1
shift
declare -i ss_count
ss_count=1



while [ 1 ]
do
ss_count=$((ss_count+1))

sstxt=$(ss --no-header -ein dst $ip)
if [ ! -z "$sstxt" ]; then
	while read line_first; read line_second
	do  
        local_port=$(echo $line_first | awk '{print $5}{print $8}' | cut -f2 -d':'|tr -d '\n')
        current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
		echo "$local_port,$current_cwnd" >> sender-cwn-$ip-file.txt
		done <<< "$sstxt"
else
	break
fi
done
	echo  ss_count_on_running_cwn_half.sh $ss_count >> sender-cwn-ss-count-$ip.txt

bash /local/repository/endpoint-scripts/calc.sh $ip
