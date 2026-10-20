from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
RAW_PATH = BASE_DIR / "data" / "hr-resources" / "HRDataset_v14.csv"
PROCESSED_PATH = BASE_DIR / "data" / "hr-resources" / "HRDataset_v14-processed.csv"

DROP_COLS = [
    "MarriedID", "MaritalStatusID", "GenderID", "EmpStatusID",
    "DeptID", "PerfScoreID", "FromDiversityJobFairID", "PositionID",
]

GENDER_MAP = {"M": "M", "F": "F"}

YES_NO_MAP = {"Yes": 1, "No": 0, "yes": 1, "no": 0}

PERF_SCORE_MAP = {
    "PIP": 1,
    "Needs Improvement": 2,
    "Fully Meets": 3,
    "Exceeds": 4,
}

DATE_COLS = ["DOB", "DateofHire", "DateofTermination", "LastPerformanceReview_Date"]

AGE_RANGE = (18, 100)
SALARY_RANGE = (0, 500_000)


def load() -> pd.DataFrame:
    return pd.read_csv(RAW_PATH)


def validate(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "nulls": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "salary_out_of_range": int((~df["Salary"].between(*SALARY_RANGE)).sum()),
        "sex_trailing_space": int((df["Sex"] != df["Sex"].str.strip()).sum()),
        "hispanic_inconsistent": int(df["HispanicLatino"].isin(["no", "yes"]).sum()),
        "dept_trailing_space": int((df["Department"] != df["Department"].str.strip()).sum()),
    }


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.drop(columns=DROP_COLS, errors="ignore", inplace=True)

    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    df["Sex"] = df["Sex"].map(GENDER_MAP)
    df["HispanicLatino"] = df["HispanicLatino"].map(YES_NO_MAP)
    df["PerformanceScore"] = df["PerformanceScore"].map(PERF_SCORE_MAP)

    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["ManagerID"] = df["ManagerID"].fillna(0).astype(int)
    df["HasTerminated"] = df["DateofTermination"].notna().astype(int)

    df.sort_values("DateofHire", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def run() -> pd.DataFrame:
    df = load()
    report = validate(df)
    print(f"  hr-resources: {report['rows']} rows, {report['nulls']} nulls, {report['duplicates']} dupes")
    print(f"    sex_trailing={report['sex_trailing_space']}, hispanic_inconsistent={report['hispanic_inconsistent']}, dept_trailing={report['dept_trailing_space']}")

    df = clean(df)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"  -> {PROCESSED_PATH.name} ({df.shape[0]}x{df.shape[1]})")
    return df
