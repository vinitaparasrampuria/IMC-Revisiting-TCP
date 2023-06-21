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
        #local_port=$(echo $line_first | awk '{print $5}{print $8}' | cut -f2 -d':'|tr -d '\n')
        
        #local_port=$(echo $line_first | awk '{print $5}' | cut -f2 -d':')
        #ino=$(echo $line_first | grep -oP '\bino:.*(\s|$)\bsk' | awk '{print $1}' | cut -f2 -d':')
	local_port=$(echo $line_first | awk '{print $5}{print $6}' | cut -f2 -d':' | tr -d '\n');
	#rtt=$(echo $line_second | grep -oP '\brtt:.*(\s|$)\bmss' | awk '{print $1}' | cut -f2 -d':');
	#data_seg_out=$(echo $line_second | grep -oP '\bdata_segs_out:.*(\s|$)\bsend' | awk '{print $1}' | cut -f2 -d':');
	#retrans=$(echo $line_second | grep -oP '\bretrans:.*(\s|$)\brcv_space' | awk '{print $1}' | cut -f2 -d':');
        current_cwnd=$(echo $line_second | grep -oP '\bcwnd:.*(\s|$)\bbytes_acked' | awk -F '[: ]' '{print $2}')
		#echo "$local_port,$current_cwnd,$rtt,$data_seg_out,$retrans" >> sender-cwn-$ip-file.txt
		echo "$local_port,$current_cwnd,$rtt" >> sender-cwn-$ip-file.txt
		done <<< "$sstxt"
else
	break
fi
done
	echo  ss_count_on_running_cwn_half.sh $ss_count >> sender-cwn-ss-count-$ip.txt

