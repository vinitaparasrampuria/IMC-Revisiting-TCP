while [ 1 ]
do
	if [ ! -z "$(ss --no-header -ein dst 10.10.2.10)" ];
	then
	bash cwn_half.sh
	break
	fi
done
