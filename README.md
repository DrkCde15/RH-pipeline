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

### ibm-attrition
- Remove colunas constantes + `EmployeeNumber`
- Gender → M/F, binários, ordinal, one-hot
- Ordenação por `Age`

### hr-resources
- Remove IDs redundantes (`MarriedID`, `GenderID`, etc.)
- Strip espaços em `Sex`, `Department`, `HispanicLatino`
- `HispanicLatino` → binário, `PerformanceScore` → ordinal
- Parsing de datas, `HasTerminated` derivado
- Ordenação por `DateofHire`

### hr-employee
- Gender → M/F/NB/NS, binários (`Attrition`, `Overtime`)
- One-hot: `Department`, `Education_Level`, `Job_Role`, `Marital_Status`
- Validação de faixa de idade e renda
- Ordenação por `Age`

### hr-company
- Lê 4 arquivos TSV (CompanyData, Diversity, EngagementSurvey)
- Remove sentinela `12/12/2999` de `Termination_Date`
- Parsing de datas, drop colunas 100% vazias do survey
- Diversity: Gender → M/F, Education → ordinal, Race → fill "Unknown"
- Join por `EmployeeID` (4968 matched)
- Ordenação por `Start_Date`

### hr-all-in-one
- Lê 4 arquivos (employee, survey, recruitment, training)
- Strip espaços, parsing de datas (`dd-Mon-yy`)
- Gender → M/F, Performance Score → ordinal
- Deriva `HasTerminated`, `TenureDays`
- Agrega treinamentos (count, custo médio, duração)
- Join por `Employee ID` (3000 matched)
- Ordenação por `StartDate`

## Testes

```bash
python -m pytest tests/ -v
```

## Dashboard

```bash
streamlit run dashboard.py
```

Dashboard interativo com seletor de dataset (5 opções):
- IBM Attrition: visão geral, demografia, cargo, correlação
- HR Resources: status, salário, departamento
- HR Employee: visão geral, distribuições
- HR Company: demografia, salário, idade x salário
- HR All-in-One: engagement, tenure

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
