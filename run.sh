#!/bin/bash

TIME=`date +"%Y-%m-%d_%H:%M:%S"`

if [ $# -lt 1 ]; then
	echo -e " "
	echo -e " usage: ./run.sh <value>"
	echo -e " e.g: ./run.sh mac"
	exit 1;
else

	if [ ${1} = "local" ]; then
		DIR="/home/ubuntu/kidsbooks/"
	elif [ ${1} = "ubuntu" ]; then
		DIR="/home/ubuntu/kidsbooks/"
	else
		exit 1;
	fi

	#pkill -9 -ef chrome

	#sleep 5

	source ${DIR}bin/activate

	for i in {1..10}
	do
		OUTPUT=$(python3 ${DIR}books.py $i $1)
		echo -e "\n"$OUTPUT"\n"
		sleep 2
	done		

fi
