import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import BatchNormalization
from sklearn.linear_model import LogisticRegression
from sklearn.utils import class_weight
from src.validation.metrics import get_metrics
from pathlib import Path
import json


def tfidf_random_forest(inp_dir, metric_path, n_epochs, threshold):

    os.makedirs(inp_dir, exist_ok=True)
    scores = {}
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(inp_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(inp_dir, f'y_{data_type}.csv'), index_col=0)

        if data_type == 'train':
            n_inputs = data.shape[1]
            visible = Input(shape=(n_inputs,))
            e = Dense(n_inputs * 2)(visible)
            e = BatchNormalization()(e)
            e = LeakyReLU()(e)
            e = Dense(n_inputs)(e)
            e = BatchNormalization()(e)
            e = LeakyReLU()(e)
            n_bottleneck = round(float(n_inputs) / 2.0)
            bottleneck = Dense(n_bottleneck)(e)
            d = Dense(n_inputs)(bottleneck)
            d = BatchNormalization()(d)
            d = LeakyReLU()(d)
            d = Dense(n_inputs * 2)(d)
            d = BatchNormalization()(d)
            d = LeakyReLU()(d)
            output = Dense(n_inputs, activation='linear')(d)

            model = Model(inputs=visible, outputs=output)
            model.compile(optimizer='adam', loss='mse')

            print('fit...')
            model.fit(data, y, epochs=n_epochs, batch_size=16, verbose=2)

            # encode using encoder
            encoder = Model(inputs=visible, outputs=bottleneck)
            data_encoded = encoder.predict(data)

            # compute class weights
            weights = class_weight.compute_class_weight('balanced',
                                                        np.unique(y),
                                                        y.label.to_list())
            class_weights = {c: w for c, w in enumerate(weights)}

            model = LogisticRegression(class_weight=class_weights)
            model.fit(data_encoded, y)

        data_encoded = encoder.predict(data)
        precision, recall, average_precision, roc_auc = get_metrics(y_true=y,
                                                                    y_pred=clf.predict(data_encoded),
                                                                    threshold=threshold)

        print('{} set evaluation:'.format(data_type))
        print('precision:{}, recall:{}, average_precision:{}, auc:{}'.format(precision, recall, average_precision,
                                                                             roc_auc))
        scores.update({
            "{}_precision".format(data_type): precision,
            "{}_recall".format(data_type): recall,
            "{}_avg_precision".format(data_type): average_precision,
            "{}_roc_auc".format(data_type): roc_auc,
        })

        os.makedirs(Path(metric_path).parent, exist_ok=True)
        with open(metric_path, "w") as f:
            json.dump(scores, f, indent=4)
