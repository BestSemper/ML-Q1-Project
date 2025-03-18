import pandas as pd

INPUT_FILE = "processed_data/preprocessing/EMS_Incident_Dispatch_Data_Processed.csv"


OUT_DIR = "processed_data/attribute_selection_csv"
FILE_BASENAME = "EMS_Incident_Dispatch"

CLASS_ATTRIBUTE = "INCIDENT_DISPOSITION_CODE"

TRAIN_SPLIT = 0.8

ATTRIBUTE_SELECTIONS = {
    "CorrelationAttributeEval": [
        "ZIPCODE",
        "SPECIAL_EVENT_INDICATOR",
        "REOPEN_INDICATOR",
        "TRANSFER_INDICATOR",
    ],
    "OneRAttributeEval": [
        "SPECIAL_EVENT_INDICATOR",
        "REOPEN_INDICATOR",
        "TRANSFER_INDICATOR",
        "HELD_INDICATOR",
        "DISPATCH_RESPONSE_SECONDS_QY",
    ],
    "CfsSubsetEval": [
        "INITIAL_SEVERITY_LEVEL_CODE",
        "DISPATCH_RESPONSE_SECONDS_QY",
        "HELD_INDICATOR",
        "ZIPCODE",
        "REOPEN_INDICATOR",
        "SPECIAL_EVENT_INDICATOR",
        "STANDBY_INDICATOR",
        "TRANSFER_INDICATOR",
    ],
    "InfoGainAttributeEval": [
        "STANDBY_INDICATOR",
        "REOPEN_INDICATOR",
        "SPECIAL_EVENT_INDICATOR",
        "TRANSFER_INDICATOR",
    ],
    "SelfSelection": [
        "HELD_INDICATOR",
        "ZIPCODE",
        "REOPEN_INDICATOR",
        "SPECIAL_EVENT_INDICATOR",
        "STANDBY_INDICATOR",
        "TRANSFER_INDICATOR",
    ],
}


def main() -> None:
    df = pd.read_csv(INPUT_FILE)

    for selection_algorithm, attributes in ATTRIBUTE_SELECTIONS.items():
        new_df = df.drop(columns=attributes)
        
        train_df = new_df.groupby(CLASS_ATTRIBUTE).sample(frac=TRAIN_SPLIT)
        test_df = new_df.drop(train_df.index)

        train_df.to_csv(f"{OUT_DIR}/{FILE_BASENAME}_{selection_algorithm}_Train.csv", index=False)
        test_df.to_csv(f"{OUT_DIR}/{FILE_BASENAME}_{selection_algorithm}_Test.csv", index=False)


if __name__ == "__main__":
    main()
