#!/bin/bash
# Run multiple parallel instances of iperf client

# Assumes the port numbers used by the servers start at 50001 and increase
# e.g. 50001, 50002, 50003, ...
base_port=50000

# Command line input: server IP address
# E.g. 1.1.1.1
server_ip=$1
shift

# Command line input: number of clients to start
# E.g. 5
num_clients=$1
shift

# Command line input: number of clients to start
# E.g. 5

# Command line input: test duration
# E.g. 60
test_duration=$1
shift

# Command line input: base report file name
# E.g. report
report_base=$1
shift

# Optional command line input: other iperf options
# E.g. -u -b 10M
iperf_options="$*"

# Run iperf multiple times
for i in `seq 1 $num_clients`; do

	# Set server port
	server_port=$(($base_port+$i));

	# Report file includes server ip, server port and test duration
	report_file1=${report_base}-${server_ip}-${server_port}-${test_duration}-reno.txt
	report_file1=${report_base}-${server_ip}-${server_port}-${test_duration}-cubic.txt

	# Run iperf
	iperf -c $server_ip -p $server_port -P 5 -C reno -cport $server_port -t $test_duration $iperf_options &> $report_file1 &
	iperf -c $server_ip -p $server_port -P 5 -C cubic -cport $server_port -t $test_duration $iperf_options &> $report_file2 &

done