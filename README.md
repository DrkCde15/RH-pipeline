# RH Pipeline

Pipeline de análise de dados de Recursos Humanos com múltiplos datasets do Kaggle.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Datasets

```bash
python download_data.py
```

Baixa todos os datasets do Kaggle para `data/`.

| Pasta | Dataset | Kaggle |
|-------|---------|--------|
| `ibm-attrition/` | IBM HR Analytics Employee Attrition | [link](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) |
| `hr-resources/` | Human Resources Data Set | [link](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set) |
| `hr-employee/` | HR Employee Dataset | [link](https://www.kaggle.com/datasets/justinlimyin/hr-employee-dataset) |
| `hr-company/` | HR The Company | [link](https://www.kaggle.com/datasets/koluit/human-resource-data-set-the-company) |
| `hr-all-in-one/` | Employee All In One | [link](https://www.kaggle.com/datasets/ravindrasinghrana/employeedataset) |

## Pipeline de limpeza

```bash
python main.py              # roda todos
python main.py ibm-attrition  # roda um específico
```

Pipelines disponíveis: `ibm-attrition`, `hr-resources`, `hr-employee`, `hr-company`, `hr-all-in-one`

## Testes

```bash
python -m pytest tests/ -v
```

## Dashboard

```bash
streamlit run dashboard.py
```

Dashboard interativo em `http://localhost:8501` com abas:
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
│   ├── ibm-attrition/
│   ├── hr-resources/
│   ├── hr-employee/
│   ├── hr-company/
│   └── hr-all-in-one/
├── pipeline/
│   ├── ibm_attrition.py
│   ├── hr_resources.py
│   ├── hr_employee.py
│   ├── hr_company.py
│   └── hr_all_in_one.py
├── notebooks/
│   └── eda.ipynb
├── tests/
│   └── test_pipeline.py
├── dashboard.py
├── download_data.py
├── main.py
├── requirements.txt
└── README.md
```
