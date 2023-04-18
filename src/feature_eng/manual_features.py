import os
import pandas as pd


def make_model_int(model):
    try:
        return int(model)
    except:
        return 1369


def manual_feature_eng(train_test_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_dir, f'x_{data_type}.csv'),
                           index_col=0)

        data.model = data.model.apply(make_model_int)
        data['age'] = data.model.apply(lambda x: 1402-x)
        data.drop(columns='model')
        data['price_per_meter'] = data['price'] / data['size']

        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))
