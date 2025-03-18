import pandas as pd


INPUT_FILE = "data/EMS_Incident_Dispatch_Data.csv"

OUT_DIR = "processed_data/preprocessing"
OUTPUT_FILE = f"{OUT_DIR}/EMS_Incident_Dispatch_Data_Fixed.csv"
# extra arguments to provide to weka
ARGUMENT_FILE = f"{OUT_DIR}/weka_arguments.txt"

ATTRIBUTES_EXPLICIT_NOMINAL = [
    "INITIAL_CALL_TYPE",
    "FINAL_CALL_TYPE",
    "INCIDENT_DISPATCH_AREA",
    "TRANSFER_INDICATOR",
    "STANDBY_INDICATOR",
    "SPECIAL_EVENT_INDICATOR",
    "REOPEN_INDICATOR",
    "VALID_DISPATCH_RSPNS_TIME_INDC",
]


def main() -> None:
    df = pd.read_csv(INPUT_FILE)

    # convert all datetime columns to numeric
    # circumvents this:
    # java.io.IOException: Read unknown nominal value '12/01/2023 12:49:23 AM'for attribute INCIDENT_DATETIME (line: 102).
    # Try increasing the size of the memory buffer (-B option) or explicitly specify legal nominal values with the -L option.
    datetime_columns = [col for col in df.columns if "DATETIME" in col]

    # first convert column from strings to datetimes
    for col in datetime_columns:
        df[col] = pd.to_datetime(df[col], format="%m/%d/%Y %I:%M:%S %p")

    # then convert column from datetimes to ints
    for col in datetime_columns:
        df[col] = df[col].astype(int) // 10**9

    # java.io.IOException: Read unknown nominal value ARRESTfor attribute INITIAL_CALL_TYPE (line: 102).
    # Try increasing the size of the memory buffer (-B option) or explicitly specify legal nominal values with the -L option.
    # weka does not look deep enough for nominal attributes
    # provide it with the list of legal nominal values for each attribute
    attr_to_values: dict[str, list[str]] = {}
    for attr in ATTRIBUTES_EXPLICIT_NOMINAL:
        attr_to_values[attr] = df[attr].unique().tolist()

    with open(ARGUMENT_FILE, "w+") as f:
        for i, (attr, values) in enumerate(attr_to_values.items()):
            if i != 0:
                f.write(" ")
            f.write(f"-L {attr}:{','.join(values)}")

    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
