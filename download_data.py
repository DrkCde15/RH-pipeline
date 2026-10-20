import shutil
from pathlib import Path

import kagglehub

DATASET = "pavansubhasht/ibm-hr-analytics-attrition-dataset"
DEST = Path(__file__).parent / "data"

path = kagglehub.dataset_download(DATASET)

for file in Path(path).rglob("*"):
    if file.is_file():
        DEST.mkdir(parents=True, exist_ok=True)
        target = DEST / file.name
        shutil.move(str(file), str(target))
        print(f"Movido para: {target}")
