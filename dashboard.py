from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="RH Dashboard", layout="wide")

COLORS = {"Yes": "#ff6b6b", "No": "#51cf66", 0: "#51cf66", 1: "#ff6b6b"}

DATASETS = {
    "IBM Attrition": BASE_DIR / "data" / "ibm-attrition" / "HR-Employee-Attrition-processed.csv",
    "HR Resources": BASE_DIR / "data" / "hr-resources" / "HRDataset_v14-processed.csv",
    "HR Employee": BASE_DIR / "data" / "hr-employee" / "HR_Dataset-processed.csv",
    "HR Company": BASE_DIR / "data" / "hr-company" / "Company-processed.csv",
    "HR All-in-One": BASE_DIR / "data" / "hr-all-in-one" / "employee-merged-processed.csv",
}


@st.cache_data
def load_data(name: str) -> pd.DataFrame:
    return pd.read_csv(DATASETS[name])


st.title("Dashboard de RH — 5 Datasets")

dataset_name = st.sidebar.selectbox("Selecione o dataset:", list(DATASETS.keys()))
df = load_data(dataset_name)

st.sidebar.metric("Registros", f"{len(df):,}")
st.sidebar.metric("Colunas", df.shape[1])
st.sidebar.metric("Nulos", df.isnull().sum().sum())

if dataset_name == "IBM Attrition":
    tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Demografia", "Cargo", "Correlação"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Taxa de Attrition", f"{df['Attrition'].mean() * 100:.1f}%")
        c2.metric("Idade Média", f"{df['Age'].mean():.1f}")
        c3.metric("Renda Média", f"${df['MonthlyIncome'].mean():,.0f}")

        counts = df["Attrition"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index.map({0: "Não saiu", 1: "Saiu"}),
                     color=counts.index, color_discrete_map={0: "#51cf66", 1: "#ff6b6b"}, hole=0.4)
        st.plotly_chart(fig, width="stretch")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x="Age", color="Attrition", barmode="overlay",
                               color_discrete_map=COLORS, opacity=0.7, title="Idade")
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.box(df, x="Attrition", y="MonthlyIncome", color="Attrition",
                         color_discrete_map=COLORS, title="Renda")
            st.plotly_chart(fig, width="stretch")

    with tab3:
        job_cols = [c for c in df.columns if c.startswith("JobRole_")]
        job_attr = {c.replace("JobRole_", ""): df[df[c] == 1]["Attrition"].mean() * 100 for c in job_cols}
        fig = px.bar(x=list(job_attr.keys()), y=list(job_attr.values()),
                     color=list(job_attr.values()), color_continuous_scale="Reds",
                     title="Attrition por Cargo (%)")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with tab4:
        corr = df.corr(numeric_only=True)["Attrition"].drop("Attrition").abs().sort_values(ascending=False).head(10)
        fig = px.bar(x=corr.values, y=corr.index, orientation="h",
                     color=corr.values, color_continuous_scale="RdBu_r",
                     title="Top 10 Correlações")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

elif dataset_name == "HR Resources":
    tab1, tab2, tab3 = st.tabs(["Status", "Salário", "Departamento"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            counts = df["EmploymentStatus"].value_counts()
            fig = px.bar(x=counts.index, y=counts.values,
                         color=counts.values, color_continuous_scale="Viridis", title="Status")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.bar(x=["PIP", "Needs Improve", "Fully Meets", "Exceeds"],
                         y=df["PerformanceScore"].value_counts().sort_index().values,
                         color=["#ff6b6b", "#ffa94d", "#51cf66", "#339af0"], title="Performance")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")

    with tab2:
        fig = px.box(df, x="HasTerminated", y="Salary", color="HasTerminated",
                     color_discrete_map=COLORS, title="Salário x Status")
        st.plotly_chart(fig, width="stretch")

    with tab3:
        dept = df.groupby("Department")["HasTerminated"].mean() * 100
        fig = px.bar(x=dept.index, y=dept.values, color=dept.values,
                     color_continuous_scale="Reds", title="Taxa de Demissão (%)")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

elif dataset_name == "HR Employee":
    tab1, tab2 = st.tabs(["Visão Geral", "Distribuições"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(x=df["Gender"].value_counts().index, y=df["Gender"].value_counts().values,
                         color=df["Gender"].value_counts().values, color_continuous_scale="Viridis",
                         title="Gênero")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.bar(x=df["Attrition"].value_counts().index.map({0: "Não", 1: "Sim"}),
                         y=df["Attrition"].value_counts().values,
                         color=["#51cf66", "#ff6b6b"], title="Attrition")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x="Age", nbins=30, title="Idade", color_discrete_sequence=["#4dabf7"])
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.histogram(df, x="Monthly_Income", nbins=40, title="Renda", color_discrete_sequence=["#ffa94d"])
            st.plotly_chart(fig, width="stretch")

elif dataset_name == "HR Company":
    tab1, tab2, tab3 = st.tabs(["Demografia", "Salário", "Idade x Salário"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(x=df["Gender"].value_counts().index, y=df["Gender"].value_counts().values,
                         color=["#f783ac", "#4dabf7"], title="Gênero")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")
        with c2:
            fig = px.bar(x=df["Country"].value_counts().index, y=df["Country"].value_counts().values,
                         color=df["Country"].value_counts().values, color_continuous_scale="Viridis",
                         title="País")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")

    with tab2:
        fig = px.box(df, x="Department", y="Salary", color="Department", title="Salário por Dept")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with tab3:
        fig = px.scatter(df, x="Age", y="Salary", color="Gender",
                         color_discrete_map={"M": "#4dabf7", "F": "#f783ac"},
                         opacity=0.4, title="Idade x Salário",
                         render_mode="svg")
        st.plotly_chart(fig, width="stretch")

elif dataset_name == "HR All-in-One":
    tab1, tab2 = st.tabs(["Engagement", "Tenure"])

    with tab1:
        survey_cols = [c for c in df.columns if "Score" in c]
        fig = go.Figure()
        for col in survey_cols:
            fig.add_trace(go.Box(y=df[col], name=col.replace(" Score", "")))
        fig.update_layout(height=400, title="Scores de Engagement")
        st.plotly_chart(fig, width="stretch")

    with tab2:
        fig = px.histogram(df, x="TenureDays", nbins=40, title="Tenure (dias)",
                           color_discrete_sequence=["#4dabf7"])
        st.plotly_chart(fig, width="stretch")
