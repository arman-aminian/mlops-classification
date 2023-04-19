import os
import numpy as np
import pandas as pd
import nlpaug.augmenter.word as naw


def text_augmentation(sent):
    aug = naw.RandomWordAug(action='swap')
    augmented_text = aug.augment(sent)[0]
    aug = naw.RandomWordAug(action='delete')
    augmented_text = aug.augment(augmented_text)
    return augmented_text


def data_augmentation(train_test_dir, out_dir, train_set_only=True):

    os.makedirs(out_dir, exist_ok=True)
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(train_test_dir, f'y_{data_type}.csv'), index_col=0)

        if not train_set_only or data_type == 'train':
            y0 = y.value_counts()[0]
            y1 = y.value_counts()[1]
            diff = np.abs(y1 - y0)
            if y0 > y1:
                samples = data[y.label == 1].sample(diff)
            else:
                samples = data[y.label == 0].sample(diff)

            samples['desc'] = samples.desc.apply(text_augmentation)
            samples.reset_index(drop=True, inplace=True)
            data.append(samples, ignore_index=True)

        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))
        y.to_csv(os.path.join(out_dir, f'y_{data_type}.csv'))
