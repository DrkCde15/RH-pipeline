# RH Pipeline

Pipeline de análise de dados de Recursos Humanos (Attrition - IBM HR Analytics).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install kagglehub
```

## Download do dataset

```bash
python download_data.py
```

Baixa o dataset do Kaggle e move para `data/`.

Dataset: [IBM HR Analytics Employee Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

## Estrutura

```
RH-pipeline/
├── data/
│   └── HR-Employee-Attrition.csv
├── download_data.py
└── README.md
```
