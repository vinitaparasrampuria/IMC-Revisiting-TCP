ip=$1
shift

while [ 1 ]
do
#echo $(ss --no-header -ein dst $ip) >> sender-cwn1-$ip-file.txt
sstxt=$(ss --no-header -ein dst $ip)
if [ ! -z "$sstxt" ]; then
		echo "$sstxt" >> sender-cwn1-$ip-file.txt
else
	break
fi
done
