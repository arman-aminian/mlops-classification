import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def manual_feature_eng(train_test_inp_dir, out_dir):
    tf_idf_vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2))

    os.makedirs(out_dir, exist_ok=True)
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_inp_dir, f'x_{data_type}.csv'), index_col=0)

        if data_type == 'train':
            tf_idf_features = tf_idf_vectorizer.fit_transform(data.desc)
        else:
            tf_idf_features = tf_idf_vectorizer.transform(data.desc)

        columns = ['t_' + str(i) for i in np.arange(tf_idf_features.shape[1])]
        df_tfidf = pd.DataFrame(tf_idf_features.toarray(), columns=columns)
        data = data.drop(columns='desc').join(df_tfidf)
        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))