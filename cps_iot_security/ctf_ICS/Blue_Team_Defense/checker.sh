#!/bin/bash

#We have written a bash script file named 'checker.sh' to monitor the PLC codes. 
#This script takes 4 files as command line arguments. The sequence order is PLC1_Benign.st, PLC2_Benign.st, PLC1_Malicious.st, PLC2_Malicious.st. Here, file names don't matter. 
#The script should tell which malicious file you are allowed to upload.

if [ "$#" -ne 4 ]; then
    echo "Please provide all four files"
    exit 1
fi

out1=$(diff $1 $3 | wc -l)
out2=$(diff $2 $4 | wc -l)

if [ $out1 -eq 0 ]; then
    echo "You can upload $3"
else
    echo "Don't upload $3"
fi

if [ $out2 -eq 0 ]; then
        echo "You can upload $4"
else
        echo "Don't upload $4"
fi
