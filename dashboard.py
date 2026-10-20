from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "HR-Employee-Attrition.csv"

st.set_page_config(page_title="RH Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


df = load_data()

st.title("Dashboard de Attrition - RH")

tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Demografia", "Cargo & Departamento", "Satisfação"])

with tab1:
    col1, col2, col3 = st.columns(3)

    attrition_rate = (df["Attrition"] == "Yes").mean() * 100
    col1.metric("Taxa de Attrition", f"{attrition_rate:.1f}%")
    col2.metric("Total de Funcionários", f"{len(df):,}")
    col3.metric("Idade Média", f"{df['Age'].mean():.1f}")

    st.subheader("Distribuição de Attrition")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.countplot(data=df, x="Attrition", palette="Set2", ax=axes[0])
    axes[0].set_title("Contagem")

    df["Attrition"].value_counts().plot.pie(
        autopct="%1.1f%%", labels=["Não saiu", "Saiu"],
        colors=["#66b3ff", "#ff9999"], ax=axes[1], ylabel=""
    )
    axes[1].set_title("Proporção")

    st.pyplot(fig)

    st.subheader("Correlação com Attrition")
    numeric_cols = df.select_dtypes(include="number").columns
    if "Attrition_num" not in df.columns:
        df["Attrition_num"] = (df["Attrition"] == "Yes").astype(int)

    corr = df[numeric_cols.tolist() + ["Attrition_num"]].corr()["Attrition_num"].drop(
        ["Attrition_num"]
    ).sort_values(key=abs, ascending=False)

    st.bar_chart(corr.head(10))

with tab2:
    st.subheader("Attrition por Idade")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.histplot(data=df, x="Age", hue="Attrition", kde=True, palette="Set2", ax=axes[0])
    axes[0].set_title("Distribuição")

    sns.boxplot(data=df, x="Attrition", y="Age", palette="Set2", ax=axes[1])
    axes[1].set_title("Boxplot")

    st.pyplot(fig)

    st.subheader("Attrition por Gênero")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="Gender", hue="Attrition", palette="Set2", ax=ax)
    st.pyplot(fig)

    st.subheader("Renda Mensal")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", palette="Set2", ax=axes[0])
    sns.histplot(data=df, x="MonthlyIncome", hue="Attrition", kde=True, palette="Set2", ax=axes[1])
    st.pyplot(fig)

with tab3:
    st.subheader("Taxa de Attrition por Departamento")
    dept = df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).sort_values()
    fig, ax = plt.subplots(figsize=(10, 4))
    dept.plot.barh(ax=ax, color=sns.color_palette("Set2", len(dept)))
    ax.set_xlabel("%")
    st.pyplot(fig)

    st.subheader("Taxa de Attrition por Cargo")
    job = df.groupby("JobRole")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100).sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    job.plot.barh(ax=ax, color=sns.color_palette("Set2", len(job)))
    ax.set_xlabel("%")
    st.pyplot(fig)

    st.subheader("Business Travel")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.countplot(data=df, x="BusinessTravel", hue="Attrition", palette="Set2", ax=ax)
    st.pyplot(fig)

with tab4:
    cols = ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance", "RelationshipSatisfaction"]
    selected = st.multiselect("Selecione métricas:", cols, default=cols[:2])

    if selected:
        fig, axes = plt.subplots(1, len(selected), figsize=(6 * len(selected), 5))
        if len(selected) == 1:
            axes = [axes]
        for i, col in enumerate(selected):
            sns.countplot(data=df, x=col, hue="Attrition", palette="Set2", ax=axes[i])
            axes[i].set_title(col)
        st.pyplot(fig)

    st.subheader("Anos na Empresa")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(data=df, x="YearsAtCompany", hue="Attrition", kde=True, palette="Set2", ax=axes[0])
    sns.boxplot(data=df, x="Attrition", y="YearsAtCompany", palette="Set2", ax=axes[1])
    st.pyplot(fig)
