

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
cca1=$1
shift

#E.g. 10,30,50
flows=$1
shift

#2nd type of cca
cca2=$1
shift

# E.g. -u -b 10M
#iperf_options="$*"

# Run iperf multiple times
for i in `seq 1 $((num_clients-1))`; do

        # Set server port
        server_port=$(($base_port+$i));
        # Report file includes server ip, server port and test duration
        report_file=sender-${server_ip}-${server_port}-${test_duration}-${cca1}.txt

        # Run iperf3
        iperf3 -c $server_ip -p $server_port -t $test_duration -C $cca1 -P $flows --format k &>$report_file &
done
server_port=$(($base_port+$num_clients))
if [ $num_clients -ne 1 ]; then
report_file=sender-${server_ip}-$((server_port))-${test_duration}-${cca1}.txt
iperf3 -c $server_ip -p $((server_port)) -t $test_duration -C $cca1 -P $((flows-1)) --format k &>$report_file &
fi
report_file=sender-${server_ip}-$((server_port+1))-${test_duration}-${cca2}.txt
iperf3 -c $server_ip -p $((server_port+1)) -t $test_duration -C $cca2 -P 1 --format k &>$report_file &
