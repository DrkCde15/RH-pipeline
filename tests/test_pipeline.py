from pathlib import Path

import pandas as pd
import pytest

from pipeline import (
    DROP_COLS,
    clean,
    drop_duplicates,
    handle_nulls,
    load,
    validate,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Age": [25, 35, 45, 30],
            "Attrition": ["Yes", "No", "No", "Yes"],
            "Gender": ["Male", "Female", "Male", "Female"],
            "OverTime": ["Yes", "No", "No", "Yes"],
            "BusinessTravel": ["Travel_Rarely", "Non-Travel", "Travel_Frequently", "Travel_Rarely"],
            "Department": ["Sales", "HR", "R&D", "Sales"],
            "EducationField": ["Life Sciences", "Other", "Medical", "Marketing"],
            "JobRole": ["Sales Executive", "Manager", "Research Scientist", "HR"],
            "MaritalStatus": ["Single", "Married", "Divorced", "Single"],
            "EmployeeCount": [1, 1, 1, 1],
            "Over18": ["Y", "Y", "Y", "Y"],
            "StandardHours": [80, 80, 80, 80],
            "EmployeeNumber": [1, 2, 3, 4],
            "MonthlyIncome": [5000, 8000, 12000, 6000],
        }
    )


class TestLoad:
    @pytest.mark.skipif(
        not Path("data/HR-Employee-Attrition.csv").exists(),
        reason="Dataset not available",
    )
    def test_load_returns_dataframe(self):
        df = load()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


class TestClean:
    def test_drop_cols(self, sample_df):
        df = clean(sample_df)
        for col in DROP_COLS:
            assert col not in df.columns

    def test_gender_values(self, sample_df):
        df = clean(sample_df)
        assert set(df["Gender"].unique()) == {"M", "F"}

    def test_attrition_binary(self, sample_df):
        df = clean(sample_df)
        assert set(df["Attrition"].unique()) <= {0, 1}

    def test_overtime_binary(self, sample_df):
        df = clean(sample_df)
        assert set(df["OverTime"].unique()) <= {0, 1}

    def test_business_travel_ordinal(self, sample_df):
        df = clean(sample_df)
        assert df["BusinessTravel"].dtype in ("int64", "float64")
        assert df["BusinessTravel"].min() >= 0
        assert df["BusinessTravel"].max() <= 2

    def test_onehot_columns(self, sample_df):
        df = clean(sample_df)
        assert "Department_HR" in df.columns or any(c.startswith("Department_") for c in df.columns)

    def test_sorted_by_age(self, sample_df):
        df = clean(sample_df)
        ages = df["Age"].tolist()
        assert ages == sorted(ages)

    def test_no_nuls_after_clean(self, sample_df):
        df = clean(sample_df)
        assert df.isnull().sum().sum() == 0


class TestHandleNulls:
    def test_no_nuls_passthrough(self, sample_df):
        df = handle_nulls(sample_df.copy())
        assert df.isnull().sum().sum() == 0

    def test_fills_numeric_with_median(self, sample_df):
        df = sample_df.copy()
        df.loc[0, "MonthlyIncome"] = None
        df = handle_nulls(df)
        assert df["MonthlyIncome"].isnull().sum() == 0

    def test_fills_categorical_with_mode(self, sample_df):
        df = sample_df.copy()
        df.loc[0, "Department"] = None
        df = handle_nulls(df)
        assert df["Department"].isnull().sum() == 0


class TestDropDuplicates:
    def test_removes_duplicates(self, sample_df):
        df = pd.concat([sample_df, sample_df], ignore_index=True)
        assert len(df) == 8
        df = drop_duplicates(df)
        assert len(df) == 4

    def test_no_duplicates_passthrough(self, sample_df):
        df = drop_duplicates(sample_df.copy())
        assert len(df) == 4


class TestValidate:
    def test_validate_runs_without_error(self, sample_df):
        validate(sample_df)


class TestPipelineIntegration:
    @pytest.mark.skipif(
        not Path("data/HR-Employee-Attrition.csv").exists(),
        reason="Dataset not available",
    )
    def test_full_pipeline(self):
        df = load()
        assert len(df) > 0

        df = handle_nulls(df)
        df = drop_duplicates(df)
        df = clean(df)

        assert df.isnull().sum().sum() == 0
        assert df.duplicated().sum() == 0
        assert set(df["Gender"].unique()) <= {"M", "F"}
        assert df["Age"].is_monotonic_increasing
        for col in DROP_COLS:
            assert col not in df.columns
