base_port=60000

# E.g. 1.1.1.1
server_ip=$1

# E.g. 5
num_clients=$2

# E.g. 60
test_duration=$3

#E.g. reno, cubic, bbr
cca1=$4

#E.g. 10,30,50
flows=$5

#2nd type of cca
cca2=$6

#iperf3 output interval
interval=$7

omit=$8

# Run iperf multiple times
if [ $num_clients -ne 1 ]; then
        for i in `seq 1 $((num_clients-1))`; do
        
                # Set server port
                server_port=$(($base_port+$i));
                # Report file includes server ip, server port and test duration
                report_file=sender-${server_ip}-${server_port}-${test_duration}-${cca1}.txt
                # Run iperf3
                nohup iperf3 -c $server_ip -p $server_port -t $test_duration -C $cca1 -P $flows -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
        done
        
        server_port=$(($base_port+$num_clients))
        if [ $flows -ne 1 ]; then
                report_file=sender-${server_ip}-$((server_port))-${test_duration}-${cca1}.txt
                nohup iperf3 -c $server_ip -p $((server_port)) -t $test_duration -C $cca1 -P $((flows-1)) -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
                report_file=sender-${server_ip}-$((server_port+1))-${test_duration}-${cca2}.txt
                nohup iperf3 -c $server_ip -p $((server_port+1)) -t $test_duration -C $cca2 -P 1 -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
        else 
                report_file=sender-${server_ip}-$((server_port))-${test_duration}-${cca2}.txt
                nohup iperf3 -c $server_ip -p $((server_port)) -t $test_duration -C $cca2 -P 1 -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
        fi 
                
else
        server_port=$(($base_port+$num_clients))
        report_file=sender-${server_ip}-$((server_port))-${test_duration}-${cca2}.txt
        nohup iperf3 -c $server_ip -p $((server_port)) -t $test_duration -C $cca2 -P 1 -i $interval --forceflush --format k -O $omit >>$report_file  2>&1 &
fi
