ip=$1
shift

while [ 1 ]
do
	if [ ! -z "$(ss --no-header -ein dst $ip)" ];
	then
	bash cwn_half.sh $ip
	break
	fi
done
