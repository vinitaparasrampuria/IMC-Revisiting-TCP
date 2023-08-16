# Run multiple parallel instances of iperf servers

# Base port is the port number after which the ports on server will be listening 
#For ee., if base port is 50000 then it will listen on 50001,50002,50003 etc.
base_port=60000

# Command line input: number of servers
# E.g. 5
num_servers=$1
shift

# Command line input: base report file name
# E.g. report
#report_base=$1


# Run iperf multiple times
for i in `seq 1 $num_servers`; do

	# Set server port
	server_port=$(($base_port+$i));
	
	report_file=${server_port}-server.dat

	# Run iperf
	iperf3 -s -p $server_port $iperf_options -D --logfile $report_file

done
