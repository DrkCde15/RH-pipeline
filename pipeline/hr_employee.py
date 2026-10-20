from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
RAW_PATH = BASE_DIR / "data" / "hr-employee" / "HR_Dataset.csv"
PROCESSED_PATH = BASE_DIR / "data" / "hr-employee" / "HR_Dataset-processed.csv"

BINARY_MAP = {
    "Attrition": {"Yes": 1, "No": 0},
    "Overtime": {"Yes": 1, "No": 0},
}

GENDER_MAP = {
    "Male": "M",
    "Female": "F",
    "Non-binary": "NB",
    "Prefer not to say": "NS",
}

ONEHOT_COLS = ["Department", "Education_Level", "Job_Role", "Marital_Status"]

AGE_RANGE = (18, 100)
INCOME_RANGE = (0, 50_000)


def load() -> pd.DataFrame:
    return pd.read_csv(RAW_PATH)


def validate(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "nulls": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "age_out_of_range": int((~df["Age"].between(*AGE_RANGE)).sum()),
        "income_out_of_range": int((~df["Monthly_Income"].between(*INCOME_RANGE)).sum()),
        "negative_years": int((df["Years_At_Company"] < 0).sum()),
        "gender_values": sorted(df["Gender"].unique().tolist()),
    }


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Gender"] = df["Gender"].map(GENDER_MAP)

    for col, mapping in BINARY_MAP.items():
        df[col] = df[col].map(mapping)

    df = pd.get_dummies(df, columns=ONEHOT_COLS, drop_first=True, dtype=int)

    df.sort_values("Age", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def run() -> pd.DataFrame:
    df = load()
    report = validate(df)
    print(f"  hr-employee: {report['rows']} rows, {report['nulls']} nulls, {report['duplicates']} dupes")
    print(f"    age_range={report['age_out_of_range']}, income_range={report['income_out_of_range']}, gender={report['gender_values']}")

    df = clean(df)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"  -> {PROCESSED_PATH.name} ({df.shape[0]}x{df.shape[1]})")
    return df
