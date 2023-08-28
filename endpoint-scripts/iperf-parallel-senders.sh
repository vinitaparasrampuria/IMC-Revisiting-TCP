
base_port=60000

# E.g. 1.1.1.1
server_ip=$1

# E.g. 5
num_clients=$2

# E.g. 60
test_duration=$3

# E.g. reno, cubic, bbr
cca=$4

# E.g. 10,30,50
flows=$5

# E.g. 1,0.01
interval=$6

omit=$7

# Run iperf multiple times
bash /local/repository/endpoint-scripts/call_func.sh $server_ip > /dev/null 2>&1 &
for i in `seq 1 $num_clients`; do

	# Set server port
	server_port=$(($base_port+$i));
	# Report file includes server ip, server port and test duration
	report_file=sender-${server_ip}-${server_port}-${test_duration}-$cca.txt

	# Run iperf3
	#iperf3 -c $server_ip -p $server_port -t $test_duration -C $cca -P $flows -O 60 -i $interval -J &>$report_file &
  	nohup iperf3 -c $server_ip -p $server_port -t $test_duration -C $cca -P $flows -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
	# sleep $(( ( RANDOM % 12 )  + 2 ))
done
