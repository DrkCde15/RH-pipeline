from pathlib import Path

import pandas as pd
import pytest

from pipeline.ibm_attrition import (
    DROP_COLS,
    clean,
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


class TestIbmAttrition:
    @pytest.mark.skipif(
        not Path("data/ibm-attrition/HR-Employee-Attrition.csv").exists(),
        reason="Dataset not available",
    )
    def test_load(self):
        df = load()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_validate(self, sample_df):
        report = validate(sample_df)
        assert report["rows"] == 4
        assert report["nulls"] == 0
        assert report["duplicates"] == 0

    def test_drop_cols(self, sample_df):
        df = clean(sample_df)
        for col in DROP_COLS:
            assert col not in df.columns

    def test_gender(self, sample_df):
        df = clean(sample_df)
        assert set(df["Gender"].unique()) == {"M", "F"}

    def test_binary(self, sample_df):
        df = clean(sample_df)
        assert set(df["Attrition"].unique()) <= {0, 1}
        assert set(df["OverTime"].unique()) <= {0, 1}

    def test_sorted_by_age(self, sample_df):
        df = clean(sample_df)
        assert df["Age"].is_monotonic_increasing

    def test_no_nulls(self, sample_df):
        df = clean(sample_df)
        assert df.isnull().sum().sum() == 0
