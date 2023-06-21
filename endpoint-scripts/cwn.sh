ip=$1
shift

while [ 1 ]
do
sstxt=$(ss --no-header -ein dst $ip)
if [ ! -z "$sstxt" ]; then
		echo "$sstxt" >> sender-cwn1-$ip-file.txt
else
	break
fi
done
