import shutil
from pathlib import Path

import kagglehub

DEST = Path(__file__).parent / "data"

DATASETS = {
    "ibm-attrition": "pavansubhasht/ibm-hr-analytics-attrition-dataset",
    "hr-resources": "rhuebner/human-resources-data-set",
    "hr-employee": "justinlimyin/hr-employee-dataset",
    "hr-company": "koluit/human-resource-data-set-the-company",
    "hr-all-in-one": "ravindrasinghrana/employeedataset",
}


def download(name: str, dataset: str) -> None:
    print(f"Baixando: {name} ({dataset})")
    path = kagglehub.dataset_download(dataset)

    target_dir = DEST / name
    target_dir.mkdir(parents=True, exist_ok=True)

    for file in Path(path).rglob("*"):
        if file.is_file():
            target = target_dir / file.name
            shutil.move(str(file), str(target))
            print(f"  -> {target}")


def main():
    for name, dataset in DATASETS.items():
        try:
            download(name, dataset)
        except (OSError, PermissionError, ValueError) as e:
            print(f"  Erro em {name}: {e}")
    print("\nConcluído!")


if __name__ == "__main__":
    main()
