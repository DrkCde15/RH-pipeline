# RH Pipeline

Pipeline de análise de dados de Recursos Humanos (Attrition - IBM HR Analytics).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Download do dataset

```bash
python download_data.py
```

Baixa o dataset do Kaggle e move para `data/`.

Dataset: [IBM HR Analytics Employee Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

## Pipeline de limpeza

```bash
python pipeline.py
```

Gera `data/HR-Employee-Attrition-processed.csv` com:
- Remoção de colunas constantes (`EmployeeCount`, `Over18`, `StandardHours`) e `EmployeeNumber`
- Validação de nulos, duplicatas e faixas de valores
- Encoding binário (`Attrition`, `OverTime`)
- Gender convertido para `M` / `F`
- Encoding ordinal (`BusinessTravel`)
- One-hot encoding (`Department`, `EducationField`, `JobRole`, `MaritalStatus`)
- Ordenação por `Age`

## Testes

```bash
python -m pytest tests/ -v
```

## Dashboard

```bash
streamlit run dashboard.py
```

Abre dashboard interativo em `http://localhost:8501` com abas de:
- Visão Geral
- Demografia
- Cargo & Departamento
- Satisfação

## EDA

Notebook em `notebooks/eda.ipynb` com análises e visualizações.

## CI/CD

GitHub Actions roda lint (`ruff`), testes e pipeline a cada push/PR em `main`.

## Estrutura

```
RH-pipeline/
├── .github/workflows/ci.yml
├── data/
│   ├── HR-Employee-Attrition.csv
│   └── HR-Employee-Attrition-processed.csv
├── notebooks/
│   └── eda.ipynb
├── tests/
│   └── test_pipeline.py
├── dashboard.py
├── download_data.py
├── pipeline.py
├── requirements.txt
└── README.md
```
