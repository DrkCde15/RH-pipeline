from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "hr-all-in-one"
PROCESSED_PATH = BASE_DIR / "data" / "hr-all-in-one" / "employee-merged-processed.csv"

GENDER_MAP = {"Male": "M", "Female": "F"}

PERF_SCORE_MAP = {
    "PIP": 1,
    "Needs Improvement": 2,
    "Fully Meets": 3,
    "Exceeds": 4,
}

EDUCATION_MAP = {
    "High School": 1,
    "Associate's Degree": 2,
    "Bachelor's Degree": 3,
    "Master's Degree": 4,
    "PhD": 5,
}

ONEHOT_COLS = [
    "BusinessUnit", "EmployeeStatus", "EmployeeType", "PayZone",
    "EmployeeClassificationType", "TerminationType", "DepartmentType",
    "Division", "GenderCode", "RaceDesc", "MaritalDesc",
    "Performance Score", "JobFunctionDescription",
]

AGE_RANGE = (18, 100)


def load() -> dict[str, pd.DataFrame]:
    return {
        "employee": pd.read_csv(RAW_DIR / "employee_data.csv"),
        "survey": pd.read_csv(RAW_DIR / "employee_engagement_survey_data.csv"),
        "recruitment": pd.read_csv(RAW_DIR / "recruitment_data.csv"),
        "training": pd.read_csv(RAW_DIR / "training_and_development_data.csv"),
    }


def validate(data: dict[str, pd.DataFrame]) -> dict:
    emp = data["employee"]
    return {
        "employee_rows": len(emp),
        "survey_rows": len(data["survey"]),
        "recruitment_rows": len(data["recruitment"]),
        "training_rows": len(data["training"]),
        "exit_nulls": int(emp["ExitDate"].isnull().sum()),
        "term_desc_nulls": int(emp["TerminationDescription"].isnull().sum()),
        "dept_trailing": int((emp["DepartmentType"] != emp["DepartmentType"].str.strip()).sum()),
        "gender_values": sorted(emp["GenderCode"].unique().tolist()),
        "emp_ids_match_survey": len(set(emp["EmpID"]) & set(data["survey"]["Employee ID"])),
    }


def clean(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    emp = data["employee"].copy()
    survey = data["survey"].copy()
    training = data["training"].copy()

    for col in emp.select_dtypes(include=["object", "string"]).columns:
        emp[col] = emp[col].str.strip()

    emp["StartDate"] = pd.to_datetime(emp["StartDate"], format="%d-%b-%y", errors="coerce")
    emp["ExitDate"] = pd.to_datetime(emp["ExitDate"], format="%d-%b-%y", errors="coerce")
    emp["DOB"] = pd.to_datetime(emp["DOB"], format="%d-%m-%Y", errors="coerce")

    emp["GenderCode"] = emp["GenderCode"].map(GENDER_MAP)
    emp["Performance Score"] = emp["Performance Score"].map(PERF_SCORE_MAP)

    emp["HasTerminated"] = emp["ExitDate"].notna().astype(int)
    emp["TenureDays"] = (emp["ExitDate"] - emp["StartDate"]).dt.days

    emp = emp.merge(
        survey.rename(columns={"Employee ID": "EmpID"}),
        on="EmpID", how="left",
    )

    training_agg = training.groupby("Employee ID").agg(
        TrainingsAttended=("Training Date", "count"),
        AvgTrainingCost=("Training Cost", "mean"),
        TotalTrainingCost=("Training Cost", "sum"),
        AvgTrainingDuration=("Training Duration(Days)", "mean"),
    ).reset_index().rename(columns={"Employee ID": "EmpID"})

    emp = emp.merge(training_agg, on="EmpID", how="left")

    emp = pd.get_dummies(emp, columns=ONEHOT_COLS, drop_first=True, dtype=int)

    emp.sort_values("StartDate", ascending=True, inplace=True)
    emp.reset_index(drop=True, inplace=True)

    return emp


def run() -> pd.DataFrame:
    data = load()
    report = validate(data)
    print(f"  hr-all-in-one: employee={report['employee_rows']}, survey={report['survey_rows']}, training={report['training_rows']}")
    print(f"    exit_nulls={report['exit_nulls']}, term_desc_nulls={report['term_desc_nulls']}, dept_trailing={report['dept_trailing']}")
    print(f"    gender={report['gender_values']}, ids_match={report['emp_ids_match_survey']}")

    df = clean(data)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"  -> {PROCESSED_PATH.name} ({df.shape[0]}x{df.shape[1]})")
    return df
