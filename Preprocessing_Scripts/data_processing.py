import math

import pandas as pd

OUT_DIR = "processed_data/preprocessing"
INPUT_FILE = f"{OUT_DIR}/EMS_Incident_Dispatch_Data_Fixed.csv"
OUTPUT_FILE = f"{OUT_DIR}/EMS_Incident_Dispatch_Data_Processed.csv"
ARGUMENT_FILE = f"{OUT_DIR}/weka_arguments.txt"


# Attributes that are obviously useless and can safely be removed
USELESS_ATTRIBUTES = [
    # all datetimes
    "INCIDENT_DATETIME",
    "FIRST_ASSIGNMENT_DATETIME",
    "FIRST_ACTIVATION_DATETIME",
    "FIRST_ON_SCENE_DATETIME",
    "FIRST_TO_HOSP_DATETIME",
    "FIRST_HOSP_ARRIVAL_DATETIME",
    "INCIDENT_CLOSE_DATETIME",
    # incident id
    "CAD_INCIDENT_ID",
    # location information
    "BOROUGH",
    "INCIDENT_DISPATCH_AREA",
    "POLICEPRECINCT",
    "CITYCOUNCILDISTRICT",
    "COMMUNITYDISTRICT",
    "COMMUNITYSCHOOLDISTRICT",
    "CONGRESSIONALDISTRICT",
]

# key verifies the data in column and should be adjusted accordingly
COLUMN_VERIFIERS = {
    "VALID_INCIDENT_RSPNS_TIME_INDC": "INCIDENT_RESPONSE_SECONDS_QY",
    "VALID_DISPATCH_RSPNS_TIME_INDC": "DISPATCH_RESPONSE_SECONDS_QY",
}

# class attribute
CLASS_ATTRIBUTE = "INCIDENT_DISPOSITION_CODE"

# attributes to force to be nominal
FORCE_NOMINAL = ["ZIPCODE", "INITIAL_SEVERITY_LEVEL_CODE", "FINAL_SEVERITY_LEVEL_CODE"]


def main() -> None:
    df = pd.read_csv(INPUT_FILE)

    # remove useless attributes
    for attr in USELESS_ATTRIBUTES:
        del df[attr]

    # drop all instances with class labels
    df.drop(df[df[CLASS_ATTRIBUTE].isna()].index, inplace=True)

    # handle verifiers
    for verifier, column in COLUMN_VERIFIERS.items():
        df.loc[df[verifier] == "N", column] = math.nan

        del df[verifier]

    # replace missing values with median
    for col in df.columns:
        na_mask = df[col].isna()

        if na_mask.sum() != 0:
            df.fillna({col: df[col].median()}, inplace=True)

    # move class attribute to the end to make it a class attribute
    df.insert(len(df.columns) - 1, CLASS_ATTRIBUTE, df.pop(CLASS_ATTRIBUTE))

    # force class attribute nominal
    df[CLASS_ATTRIBUTE] = df[CLASS_ATTRIBUTE].astype(int)

    # force other attributes nominal
    for attr in FORCE_NOMINAL:
        df[attr] = df[attr].astype(int)

    with open(ARGUMENT_FILE, "a") as f:
        f.write(
            f" -L {CLASS_ATTRIBUTE}:{','.join(map(str, df[CLASS_ATTRIBUTE].unique()))}"
        )
        for attr in FORCE_NOMINAL:
            f.write(f" -L {attr}:{','.join(map(str, df[attr].unique()))}")

    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
