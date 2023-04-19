import argparse
import yaml
from src.collect_data.unificate_data import data_unification
from src.collect_data.split_data import split_dataset
from src.feature_eng.manual_features import manual_feature_eng
from src.feature_eng.tfidf_features import tfidf_eng
from src.tfidf_random_forest.random_forest import tfidf_random_forest


def main():
    job_table = {
        'transfer_to_sql_and_unificate_data': data_unification,
        'split_data': split_dataset,
        'manual_feature_eng': manual_feature_eng,
        'tf_idf_eng': tfidf_eng,
        'random_forest': tfidf_random_forest
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--job', required=True, type=str, choices=job_table.keys())

    args = parser.parse_args()
    params = yaml.safe_load(open('params.yaml'))[args.job]
    print(params)

    job_table[args.job](**params)


if __name__ == '__main__':
    main()
