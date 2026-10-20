from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
RAW_PATH = BASE_DIR / "data" / "ibm-attrition" / "HR-Employee-Attrition.csv"
PROCESSED_PATH = BASE_DIR / "data" / "ibm-attrition" / "HR-Employee-Attrition-processed.csv"

DROP_COLS = ["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"]

BINARY_MAP = {
    "Attrition": {"Yes": 1, "No": 0},
    "OverTime": {"Yes": 1, "No": 0},
}

ORDINAL_MAPS = {
    "BusinessTravel": {
        "Non-Travel": 0,
        "Travel_Rarely": 1,
        "Travel_Frequently": 2,
    },
}

ONEHOT_COLS = ["Department", "EducationField", "JobRole", "MaritalStatus"]

GENDER_MAP = {"Male": "M", "Female": "F"}

AGE_RANGE = (18, 100)


def load() -> pd.DataFrame:
    return pd.read_csv(RAW_PATH)


def validate(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "nulls": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "age_out_of_range": int((~df["Age"].between(*AGE_RANGE)).sum()),
        "negative_income": int((df["MonthlyIncome"] < 0).sum()),
        "gender_invalid": len(set(df["Gender"].unique()) - {"Male", "Female"}),
    }


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.drop(columns=DROP_COLS, errors="ignore", inplace=True)

    df["Gender"] = df["Gender"].map(GENDER_MAP)

    for col, mapping in BINARY_MAP.items():
        df[col] = df[col].map(mapping)

    for col, mapping in ORDINAL_MAPS.items():
        df[col] = df[col].map(mapping)

    df = pd.get_dummies(df, columns=ONEHOT_COLS, drop_first=True, dtype=int)

    df.sort_values("Age", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def run() -> pd.DataFrame:
    df = load()
    report = validate(df)
    print(f"  ibm-attrition: {report['rows']} rows, {report['nulls']} nulls, {report['duplicates']} dupes")

    df = clean(df)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"  -> {PROCESSED_PATH.name} ({df.shape[0]}x{df.shape[1]})")
    return df
