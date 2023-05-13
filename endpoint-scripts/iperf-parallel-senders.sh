
base_port=60000

# E.g. 1.1.1.1
server_ip=$1
shift

# E.g. 5
num_clients=$1
shift

# E.g. 60
test_duration=$1
shift

# E.g. report
#report_base=$1
#shift

#E.g. reno, cubic, bbr
cca=$1
shift

#E.g. 10,30,50
flows=$1
shift

# E.g. -u -b 10M
iperf_options="$*"

# Run iperf multiple times
for i in `seq 1 $num_clients`; do

	# Set server port
	server_port=$(($base_port+$i));
	# Report file includes server ip, server port and test duration
	report_file=sender-${server_ip}-${server_port}-${test_duration}-$cca.txt

	# Run iperf3
	iperf3 -c $server_ip -p $server_port -t $test_duration -C $cca -P $flows --format k &>$report_file &
done