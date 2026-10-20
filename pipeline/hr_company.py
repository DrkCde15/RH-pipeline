from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "hr-company"
PROCESSED_PATH = BASE_DIR / "data" / "hr-company" / "Company-processed.csv"

SENTINEL_DATE = "12/12/2999"

GENDER_MAP = {"female": "F", "male": "M"}

EDUCATION_MAP = {
    "High School": 1,
    "Some College": 2,
    "Undergraduate": 3,
    "Graduate": 4,
    "PhD": 5,
}

ORIENTATION_MAP = {
    "Heterosexual": 0,
    "Bisexual": 1,
    "Gay": 2,
    "Lesbian": 3,
    "Other LGBTQ+": 4,
    "Missing": -1,
}

AGE_RANGE = (18, 100)
SALARY_RANGE = (0, 1_000_000)


def load() -> dict[str, pd.DataFrame]:
    return {
        "company": pd.read_csv(RAW_DIR / "CompanyData.csv", sep="\t"),
        "diversity": pd.read_csv(RAW_DIR / "Diversity.csv", sep="\t"),
        "survey": pd.read_csv(RAW_DIR / "EngagementSurvey.csv", sep="\t"),
    }


def validate(data: dict[str, pd.DataFrame]) -> dict:
    company = data["company"]
    diversity = data["diversity"]
    survey = data["survey"]

    return {
        "company_rows": len(company),
        "diversity_rows": len(diversity),
        "survey_rows": len(survey),
        "company_nulls": int(company.isnull().sum().sum()),
        "diversity_nulls": int(diversity.isnull().sum().sum()),
        "survey_nulls": int(survey.isnull().sum().sum()),
        "address_nulls": int(company[["StreetAddress", "City", "State"]].isnull().any(axis=1).sum()),
        "race_nulls": int(diversity["Race/Ethnicity"].isnull().sum()),
        "sentinel_dates": int((company["Termination_Date"] == SENTINEL_DATE).sum()),
        "ids_match": len(set(company["EmployeeID"]) & set(diversity["EmployeeID"])),
        "empty_survey_cols": [
            c for c in survey.columns if survey[c].isnull().all()
        ],
    }


def clean(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    company = data["company"].copy()
    diversity = data["diversity"].copy()
    survey = data["survey"].copy()

    for col in company.select_dtypes(include=["object", "string"]).columns:
        company[col] = company[col].str.strip()

    company["Termination_Date"] = company["Termination_Date"].replace(SENTINEL_DATE, None)
    company["Start_Date"] = pd.to_datetime(company["Start_Date"], errors="coerce")
    company["Termination_Date"] = pd.to_datetime(company["Termination_Date"], errors="coerce")
    company["DOB"] = pd.to_datetime(company["DOB"], errors="coerce")

    company["Age"] = company["Age"].clip(AGE_RANGE[0], AGE_RANGE[1])

    diversity["Gender"] = diversity["Gender"].map(GENDER_MAP)
    diversity["Education"] = diversity["Education"].map(EDUCATION_MAP)
    diversity["Sexual Orientation"] = diversity["Sexual Orientation"].map(ORIENTATION_MAP)
    diversity["Race/Ethnicity"] = diversity["Race/Ethnicity"].fillna("Unknown")

    empty_cols = [c for c in survey.columns if survey[c].isnull().all()]
    survey.drop(columns=empty_cols, errors="ignore", inplace=True)

    df = company.merge(diversity, on="EmployeeID", how="left")
    df = df.merge(survey, on="EmployeeID", how="left")

    df["HasTerminated"] = df["Termination_Date"].notna().astype(int)

    df.sort_values("Start_Date", ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def run() -> pd.DataFrame:
    data = load()
    report = validate(data)
    print(f"  hr-company: company={report['company_rows']}, diversity={report['diversity_rows']}, survey={report['survey_rows']}")
    print(f"    nulls: company={report['company_nulls']}, diversity={report['diversity_nulls']}, survey={report['survey_nulls']}")
    print(f"    address_nulls={report['address_nulls']}, race_nulls={report['race_nulls']}, sentinel_dates={report['sentinel_dates']}")
    print(f"    ids_match={report['ids_match']}, empty_cols={report['empty_survey_cols']}")

    df = clean(data)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"  -> {PROCESSED_PATH.name} ({df.shape[0]}x{df.shape[1]})")
    return df
