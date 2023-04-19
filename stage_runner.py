import argparse
import yaml
from src.collect_data.unificate_data import data_unification
from src.collect_data.split_data import split_dataset
from src.feature_eng.manual_features import manual_feature_eng
from src.feature_eng.tfidf_features import tfidf_eng
from src.tfidf_random_forest.random_forest import tfidf_random_forest
from src.autoencoder_logistic_regression.autoencoder_logistic_regression import autoencoder_logistic_regression_class_weights
from src.balance_data.data_augmentation import data_augmentation
from src.feature_eng.bert_encoding import bert_encoding
from src.feature_eng.char_vectorizer import char_vectorizer


def main():
    job_table = {
        'transfer_to_sql_and_unificate_data': data_unification,
        'split_data': split_dataset,
        'manual_feature_eng': manual_feature_eng,
        'tf_idf_eng': tfidf_eng,
        'random_forest': tfidf_random_forest,
        'autoencoder_logistic_regression': autoencoder_logistic_regression_class_weights,
        'data_augmentation': data_augmentation,
        'bert_encoding': bert_encoding,
        'char_vect_eng': char_vectorizer
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--job', required=True, type=str, choices=job_table.keys())

    args = parser.parse_args()
    params = yaml.safe_load(open('params.yaml'))[args.job]
    print(params)

    job_table[args.job](**params)


if __name__ == '__main__':
    main()
