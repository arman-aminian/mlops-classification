import os
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from src.validation.metrics import get_metrics
from pathlib import Path
import json


def bert_gradient_boost(inp_dir, metric_path, n_estimators, threshold):
    clf = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=0.1, max_depth=2)

    os.makedirs(inp_dir, exist_ok=True)
    scores = {}
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(inp_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(inp_dir, f'y_{data_type}.csv'), index_col=0)

        if data_type == 'train':
            clf.fit(data, y)

        precision, recall, average_precision, roc_auc = get_metrics(y_true=y,
                                                                    y_pred=clf.predict(data),
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

