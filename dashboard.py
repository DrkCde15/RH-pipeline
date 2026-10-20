from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "HR-Employee-Attrition.csv"

st.set_page_config(page_title="RH Dashboard", layout="wide")

COLORS = {"Yes": "#ff6b6b", "No": "#51cf66"}


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


df = load_data()

st.title("Dashboard de Attrition - RH")

tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Demografia", "Cargo & Departamento", "Satisfação"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)

    attrition_rate = (df["Attrition"] == "Yes").mean() * 100
    col1.metric("Taxa de Attrition", f"{attrition_rate:.1f}%")
    col2.metric("Total de Funcionários", f"{len(df):,}")
    col3.metric("Idade Média", f"{df['Age'].mean():.1f}")
    col4.metric("Renda Média", f"${df['MonthlyIncome'].mean():,.0f}")

    st.subheader("Distribuição de Attrition")
    col1, col2 = st.columns(2)

    with col1:
        counts = df["Attrition"].value_counts()
        fig = px.pie(
            values=counts.values,
            names=counts.index.map({"Yes": "Saiu", "No": "Não saiu"}),
            color=counts.index,
            color_discrete_map={"Yes": COLORS["Yes"], "No": COLORS["No"]},
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            x=counts.index.map({"Yes": "Saiu", "No": "Não saiu"}),
            y=counts.values,
            color=counts.index,
            color_discrete_map=COLORS,
            labels={"x": "Attrition", "y": "Contagem"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Correlações com Attrition")
    df["Attrition_num"] = (df["Attrition"] == "Yes").astype(int)
    numeric_cols = df.select_dtypes(include="number").columns.drop("Attrition_num")
    corr = df[numeric_cols.tolist() + ["Attrition_num"]].corr()["Attrition_num"].drop(
        "Attrition_num"
    ).sort_values(key=abs, ascending=False).head(10)

    fig = px.bar(
        x=corr.values,
        y=corr.index,
        orientation="h",
        color=corr.values,
        color_continuous_scale="RdBu_r",
        labels={"x": "Correlação", "y": ""},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Attrition por Idade")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df, x="Age", color="Attrition", barmode="overlay",
            nbins=30, color_discrete_map=COLORS, opacity=0.7,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            df, x="Attrition", y="Age", color="Attrition",
            color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Attrition por Gênero")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df, x="Gender", color="Attrition",
            barmode="group", color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        gender_rate = df.groupby("Gender")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
        fig = px.bar(
            x=gender_rate.index, y=gender_rate.values,
            color=gender_rate.index, color_discrete_sequence=["#4dabf7", "#f783ac"],
            labels={"x": "Gênero", "y": "Taxa de Attrition (%)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Renda Mensal")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            df, x="Attrition", y="MonthlyIncome", color="Attrition",
            color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            df, x="MonthlyIncome", color="Attrition",
            barmode="overlay", nbins=40, color_discrete_map=COLORS, opacity=0.7,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Taxa de Attrition por Departamento")
    dept = (
        df.groupby("Department")["Attrition"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .reset_index()
        .rename(columns={"Attrition": "Taxa (%)"})
    )
    fig = px.bar(
        dept, x="Taxa (%)", y="Department", orientation="h",
        color="Taxa (%)", color_continuous_scale="Reds",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Taxa de Attrition por Cargo")
    job = (
        df.groupby("JobRole")["Attrition"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .reset_index()
        .rename(columns={"Attrition": "Taxa (%)"})
    )
    fig = px.bar(
        job, x="Taxa (%)", y="JobRole", orientation="h",
        color="Taxa (%)", color_continuous_scale="Reds",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Business Travel")
        fig = px.histogram(
            df, x="BusinessTravel", color="Attrition",
            barmode="group", color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Education Field")
        fig = px.histogram(
            df, x="EducationField", color="Attrition",
            barmode="group", color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    cols = ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance", "RelationshipSatisfaction"]
    selected = st.multiselect("Selecione métricas:", cols, default=cols[:2])

    if selected:
        col1, col2 = st.columns(2)
        for i, col in enumerate(selected):
            with (col1 if i % 2 == 0 else col2):
                fig = px.histogram(
                    df, x=col, color="Attrition",
                    barmode="group", color_discrete_map=COLORS,
                )
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("Anos na Empresa")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df, x="YearsAtCompany", color="Attrition",
            barmode="overlay", nbins=20, color_discrete_map=COLORS, opacity=0.7,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            df, x="Attrition", y="YearsAtCompany", color="Attrition",
            color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Over Time")
    fig = px.histogram(
        df, x="OverTime", color="Attrition",
        barmode="group", color_discrete_map=COLORS,
    )
    st.plotly_chart(fig, use_container_width=True)
