ip=$1
shift
declare -A cwnd_dict
declare -A halving_dict
declare -i ss_count
ss_count=1


sstxt=$(cat sender-cwn-$ip-file.txt)
while read line
do
ss_count=$((ss_count+1))
local_port=$(echo $line | awk -F '[, ]' '{print $1}')
current_cwnd=$(echo $line |  awk -F '[, ]' '{print $2}')
prev_cwnd=$((${cwnd_dict[$local_port]}))
	if [ ! -v halving_dict[$local_port] ]; then
			halving_dict[$local_port]=0
		fi
		if [[ ! -z "$prev_cwnd" ]] && [[ "$current_cwnd" -lt "$prev_cwnd" ]]; then
			((halving_dict[$local_port]++))
		fi
		cwnd_dict[$local_port]=$current_cwnd
		done <<< "$sstxt"
echo tolat ss_count is $ss_count >> sender-cwn-ss-count-$ip.txt

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
	echo $((ss_count)) >> sender-cwn-ss-count-$ip.txt
