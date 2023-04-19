import os
import pandas as pd
from hazm import Normalizer, Stemmer, Lemmatizer, WordTokenizer
import emoji


def make_model_int(model):
    try:
        return int(model)
    except:
        return 1369


def preprocess_description(text, tokenizer, normalizer, lemmatizer):

    # remove emojies
    text = emoji.get_emoji_regexp().sub(r'', text)
    # tokenize - replace link-number-
    words = tokenizer.tokenize(' '.join(tokenizer.tokenize(text)))
    # replace ي with ی and remove arabic symbols
    words = [normalizer.character_refinement(word) for word in words]

    text = ' '.join([lemmatizer.lemmatize(word) for word in words])
    return text


def manual_feature_eng(train_test_dir, out_dir):
    tokenizer = WordTokenizer(join_verb_parts=False, replace_links=True, replace_numbers=True)
    normalizer = Normalizer()
    lemmatizer = Lemmatizer()

    os.makedirs(out_dir, exist_ok=True)
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(train_test_dir, f'y_{data_type}.csv'), index_col=0)

        data.model = data.model.apply(make_model_int)
        data['age'] = data.model.apply(lambda x: 1402 - x)
        data.drop(columns='model')
        data['price_per_meter'] = data['price'] / data['size']
        data['desc'] = data.desc.apply(lambda x: preprocess_description(x, tokenizer, normalizer, lemmatizer))

        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))
        y.to_csv(os.path.join(out_dir, f'y_{data_type}.csv'))
