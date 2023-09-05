ip=$1
shift

sleep 120

while [ 1 ]
do
#echo $(ss --no-header -ein dst $ip) >> sender-cwn1-$ip-file.txt
sstxt=$(ss --no-header -ein dst $ip)
if [ ! -z "$sstxt" ]; then
		echo "$sstxt" >> sender-cwn1-$ip-file.txt
		sleep 1
else
	break
fi
done
