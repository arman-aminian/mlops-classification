import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def make_model_int(model):
    try:
        return int(model)
    except:
        return 1369


def char_vectorizer(train_test_inp_dir, out_dir):
    char_vect = CountVectorizer(ngram_range=(2, 2), analyzer="char")

    os.makedirs(out_dir, exist_ok=True)
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_inp_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(train_test_inp_dir, f'y_{data_type}.csv'), index_col=0)

        data.model = data.model.apply(make_model_int)

        if data_type == 'train':
            tf_idf_features = char_vect.fit_transform(data.desc)
        else:
            tf_idf_features = char_vect.transform(data.desc)

        columns = ['c_' + str(i) for i in np.arange(tf_idf_features.shape[1])]
        df_tfidf = pd.DataFrame(tf_idf_features.toarray(), columns=columns)
        data = data.drop(columns='desc').join(df_tfidf)
        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))
        y.to_csv(os.path.join(out_dir, f'y_{data_type}.csv'))
