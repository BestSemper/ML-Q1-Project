#!/bin/bash

set -e

mkdir -p processed_data/preprocessing

echo "Running \"format_for_arff.py\""
python3 format_for_arff.py
echo "Running \"data_processing.py\""
python3 data_processing.py

WEKA_ARGS="$(cat processed_data/preprocessing/weka_arguments.txt)"

PROCESSED_FILE="processed_data/preprocessing/EMS_Incident_Dispatch_Data_Processed"

echo "Converting \"$(basename $PROCESSED_FILE.csv)\" to arff format"
../shared/csv_to_arff.sh "$PROCESSED_FILE.csv" "$PROCESSED_FILE.arff" $WEKA_ARGS


mkdir -p processed_data/attribute_selection_csv
mkdir -p processed_data/attribute_selection_arff

echo "Running \"train_test_split.py\""
python3 train_test_split.py

for csv in ./processed_data/attribute_selection_csv/*; do
    csv_name=$(basename $csv .csv)
    echo "Converting \"$csv_name.arff\" to arff format"
    ../shared/csv_to_arff.sh "$csv" "processed_data/attribute_selection_arff/$csv_name.arff" $WEKA_ARGS
done
