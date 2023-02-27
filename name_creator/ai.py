import random
import numpy as np
import os
import json
import re
from itertools import islice
from tensorflow.python.ops.numpy_ops.np_random import seed
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential as Seq
from keras.utils import to_categorical
from keras.layers import LSTM, Dense, Dropout

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
seed(69)

names = open('names.txt', 'r').read().splitlines()
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(names)
char_to_int = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(names)
max_length = max([len(it) for it in sequences])
end_of_names = ('l', 't', 'h', 's', 'r', 'm', 'y', 'x', 'n', 'f', 'k', 'a', 'e', 'i', 'o', 'u')

x = np.array([seq + [0] * (max_length - len(seq)) for seq in sequences])
x = to_categorical(x)
y = np.zeros_like(x)
y = to_categorical(y)
y = np.squeeze(y, axis=-1)

model = Seq()
model.add(LSTM(128, activation='relu', input_shape=(max_length, len(char_to_int) + 1), return_sequences=True))
model.add(Dropout(0.1))
model.add(Dense(len(char_to_int) + 1, activation='sigmoid'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.load_weights('model.h5')


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_name(seed_txt: str, temperature: float = 1.0, times: int = 1):
    while True:
        generated = ""
        for i in range(random.randint(3, max_length - len(seed_txt))):
            x_pred = np.zeros((1, max_length, len(char_to_int.keys()) + 1))
            for t, char in enumerate(seed_txt.lower()):
                x_pred[0, t, char_to_int[char]] = 1.0
            preds = model.predict(x_pred, verbose=0)[0][0]
            next_index = sample(preds, temperature)
            if next_index == 0:
                next_char = list(char_to_int.keys())[0]
            else:
                next_char = list(char_to_int.keys())[list(char_to_int.values()).index(next_index)]
                if next_char in ['', "'", '-']:
                    continue
            generated += next_char
        generated_check = re.findall(r'[bcdfghjklmnpqrstvwxyz]+', generated, re.IGNORECASE)

        def coc(string):
            return bool(re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', string, re.IGNORECASE))
        for item in generated_check:
            if len(generated_check) == 1 and len(item) <= 2 and coc(generated) is False:
                if item.endswith(end_of_names):
                    return f"{seed_txt}{generated.replace(' ', '')}"
