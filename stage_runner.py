import argparse
import yaml
from src.collect_data.unificate_data import data_unification
from src.collect_data.split_data import split_dataset


def main():
    job_table = {
        'transfer_to_sql_and_unificate_data': data_unification,
        'split_data': split_dataset
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--job', required=True, type=str, choices=job_table.keys())

    args = parser.parse_args()
    params = yaml.safe_load(open('params.yaml'))[args.job]
    print(params)

    job_table[args.job](**params)


if __name__ == '__main__':
    main()
