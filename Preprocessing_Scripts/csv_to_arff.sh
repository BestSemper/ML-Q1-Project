#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Usage: ./csv_to_arff.sh [Input File] [Output File] [... Args To Pass to Weka]"
    exit 1
fi

java -cp "$(dirname $0)/weka_stable_3.8.6.jar" weka.core.converters.CSVLoader $1 ${@:3:$#} > $2
