from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
RAW_PATH = BASE_DIR / "data" / "HR-Employee-Attrition.csv"
PROCESSED_PATH = BASE_DIR / "data" / "HR-Employee-Attrition-processed.csv"

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
INCOME_RANGE = (0, None)
PERCENT_RANGE = (0, 100)


def load(path: Path = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def validate(df: pd.DataFrame) -> None:
    print(f"Linhas: {len(df)}, Colunas: {len(df.columns)}")

    nulos = df.isnull().sum().sum()
    print(f"Nulos: {nulos}")

    dup = df.duplicated().sum()
    print(f"Duplicatas: {dup}")

    if "Age" in df.columns:
        fora = ~df["Age"].between(*AGE_RANGE)
        print(f"Idade fora de [{AGE_RANGE[0]}, {AGE_RANGE[1]}]: {fora.sum()}")

    if "MonthlyIncome" in df.columns:
        neg = (df["MonthlyIncome"] < 0).sum()
        print(f"Renda mensal negativa: {neg}")

    for col in ["DistanceFromHome", "JobSatisfaction", "WorkLifeBalance",
                "EnvironmentSatisfaction", "JobInvolvement", "PerformanceRating"]:
        if col in df.columns:
            neg = (df[col] < 0).sum()
            if neg:
                print(f"{col} negativo: {neg}")

    if "Gender" in df.columns:
        validos = {"M", "F"}
        invalidos = set(df["Gender"].unique()) - validos
        if invalidos:
            print(f"Gender inválido: {invalidos}")

    print()


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removidas = antes - len(df)
    if removidas:
        print(f"Duplicatas removidas: {removidas}")
    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    nulos = df.isnull().sum()
    cols_com_nulos = nulos[nulos > 0]
    if cols_com_nulos.empty:
        print("Nulos: nenhum")
        return df

    print("Nulos por coluna:")
    print(cols_com_nulos.to_string())

    for col in cols_com_nulos.index:
        if df[col].dtype in ("int64", "float64"):
            mediana = df[col].median()
            df[col].fillna(mediana, inplace=True)
            print(f"  {col}: preenchido com mediana ({mediana})")
        else:
            moda = df[col].mode()[0]
            df[col].fillna(moda, inplace=True)
            print(f"  {col}: preenchido com moda ({moda})")

    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.drop(columns=DROP_COLS, errors="ignore", inplace=True)

    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].map(GENDER_MAP)

    for col, mapping in BINARY_MAP.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    for col, mapping in ORDINAL_MAPS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    df = pd.get_dummies(df, columns=ONEHOT_COLS, drop_first=True, dtype=int)

    if "Age" in df.columns:
        df.sort_values("Age", ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        print("Ordenado por Age (crescente)")

    return df


def main():
    df = load()
    print("=== Validação (raw) ===")
    validate(df)

    df = handle_nulls(df)
    df = drop_duplicates(df)

    print("=== Limpeza ===")
    df = clean(df)

    print("\n=== Validação (processed) ===")
    validate(df)

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Salvo em: {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
