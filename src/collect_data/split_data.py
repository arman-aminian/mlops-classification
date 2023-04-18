import os
import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(file_path, train_test_dir):

    # concatenate dataframes
    data = pd.read_csv(file_path,
                       on_bad_lines='skip',
                       delimiter=';',
                       names=['model', 'desc', 'price', 'size', 'label'])

    y = data['label'].apply(lambda x: int(x.split('.')[0] == 'house_tehran'))
    X = data.drop(columns='label')

    # split data to train / test / validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=1)

    # save train / test / validation
    os.makedirs(train_test_dir, exist_ok=True)

    X_train.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'x_train.csv'))
    y_train.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'y_train.csv'))
    X_test.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'x_test.csv'))
    y_test.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'y_test.csv'))
    X_val.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'x_val.csv'))
    y_val.reset_index(drop=True).to_csv(os.path.join(train_test_dir, 'y_val.csv'))

