import sys

from pipeline import hr_all_in_one, hr_company, hr_employee, hr_resources, ibm_attrition

PIPELINES = {
    "ibm-attrition": ibm_attrition.run,
    "hr-resources": hr_resources.run,
    "hr-employee": hr_employee.run,
    "hr-company": hr_company.run,
    "hr-all-in-one": hr_all_in_one.run,
}


def main():
    targets = sys.argv[1:] or list(PIPELINES.keys())

    for name in targets:
        if name not in PIPELINES:
            print(f"Pipeline desconhecido: {name}")
            print(f"Disponíveis: {', '.join(PIPELINES.keys())}")
            continue

        print(f"\n{'='*50}")
        print(f"  Pipeline: {name}")
        print(f"{'='*50}")
        try:
            PIPELINES[name]()
        except FileNotFoundError as e:
            print(f"  Dataset não encontrado: {e}")
            print("  Rode: python download_data.py")
        except (OSError, ValueError, KeyError) as e:
            print(f"  Erro: {e}")

    print("\nConcluído!")


if __name__ == "__main__":
    main()
