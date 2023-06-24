ip=$1
shift

while [ 1 ]
do
	if [ ! -z "$(ss --no-header -ein dst $ip)" ];
	then
	#bash /local/repository/endpoint-scripts/cwn_half.sh $ip
 	bash /local/repository/endpoint-scripts/cwn.sh $ip
	break
	fi
done
