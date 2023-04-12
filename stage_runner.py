import argparse
import yaml
from src.collect_data.collect_data import transfer_csv_to_postgresql


def main():
    job_table = {
        'transfer_to_sql_and_unificate_data': transfer_csv_to_postgresql,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--job', required=True, type=str, choices=job_table.keys())

    args = parser.parse_args()
    params = yaml.safe_load(open('params.yaml'))[args.job]
    print(params)

    job_table[args.job](**params)


if __name__ == '__main__':
    main()
