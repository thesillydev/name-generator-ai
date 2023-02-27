import random
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

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
