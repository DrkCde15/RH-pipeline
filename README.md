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
- Encoding binário (`Attrition`, `Gender`, `OverTime`)
- Encoding ordinal (`BusinessTravel`)
- One-hot encoding (`Department`, `EducationField`, `JobRole`, `MaritalStatus`)

## Estrutura

```
RH-pipeline/
├── data/
│   ├── HR-Employee-Attrition.csv
│   └── HR-Employee-Attrition-processed.csv
├── download_data.py
├── pipeline.py
├── requirements.txt
└── README.md
```
