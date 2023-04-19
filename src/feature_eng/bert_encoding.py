import os
import numpy as np
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel


def encode(tokenizer, model, text):
    tokens = tokenizer.encode(text, add_special_tokens=True)
    input_ids = torch.tensor([tokens])
    outputs = model(input_ids)
    last_hidden_states = outputs[0]
    embedding = torch.mean(last_hidden_states, dim=1)
    return embedding.detach().numpy().tolist()[0]


def bert_encoding(train_test_inp_dir, out_dir, min_df):
    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('HooshvareLab/bert-fa-zwnj-base')
    model = BertModel.from_pretrained('HooshvareLab/bert-fa-zwnj-base')

    os.makedirs(out_dir, exist_ok=True)
    for data_type in ['train', 'test', 'val']:
        # read file
        data = pd.read_csv(os.path.join(train_test_inp_dir, f'x_{data_type}.csv'), index_col=0)
        y = pd.read_csv(os.path.join(train_test_inp_dir, f'y_{data_type}.csv'), index_col=0)

        bert_embeddings = data.desc.apply(lambda x: encode(tokenizer, model, x))

        columns = ['t_' + str(i) for i in np.arange(bert_embeddings.shape[1])]
        df_tfidf = pd.DataFrame(bert_embeddings.tolist(), columns=columns)
        data = data.drop(columns='desc').join(df_tfidf)
        data.to_csv(os.path.join(out_dir, f'x_{data_type}.csv'))
        y.to_csv(os.path.join(out_dir, f'y_{data_type}.csv'))
