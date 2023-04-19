import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from src.validation.metrics import get_metrics
from pathlib import Path
import json


def pca_logistic_regression(inp_dir, metric_path, threshold):
    pca = PCA(n_components=200)
    model = LogisticRegression()

    os.makedirs(inp_dir, exist_ok=True)
    scores = {}
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(inp_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(inp_dir, f'y_{data_type}.csv'), index_col=0)

        if data_type == 'train':
            # down scale data
            y0 = y.value_counts()[0]
            y1 = y.value_counts()[1]
            n_min = min(y1, y0)
            if y0 > y1:
                samples = data[y.label == 0].sample(n_min)
                data[y.label == 1].append(samples, ignore_index=True)
            else:
                samples = data[y.label == 1].sample(n_min)
                data[y.label == 0].append(samples, ignore_index=True)

            data_pca = pca.fit_transform(data)
            model.fit(data_pca, y)

        data = pca.transform(data)

        precision, recall, average_precision, roc_auc = get_metrics(y_true=y,
                                                                    y_pred=model.predict(data),
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

