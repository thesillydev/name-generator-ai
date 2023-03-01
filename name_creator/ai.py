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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Removes unnecessary warning
seed(69) # Set seed for reproducibility

names = open('names.txt', 'r').read().splitlines() 
tokenizer = Tokenizer(char_level=True)  # Convert the characters of all strings into numbers
tokenizer.fit_on_texts(names)
char_to_int = tokenizer.word_index  # Creates a dict similar to this {'a': 1, 'b': 2, 'c': 3, ...} to make it easier to do previsions
sequences = tokenizer.texts_to_sequences(names)  # Creates an array of total sequences
max_length = max([len(it) for it in sequences])  # Pick the length of the biggest name
end_of_names = ('l', 't', 'h', 's', 'r', 'm', 'y', 'x', 'n', 'f', 'k', 'w', 'a', 'e', 'i', 'o', 'u')  # Parameter to generate more accurate names, 
#  since it can create names that ends with j or q or some unexpecting character ending

# Creates the X and Y parameter and convert to categorical
x = np.array([seq + [0] * (max_length - len(seq)) for seq in sequences])  
x = to_categorical(x)
y = np.zeros_like(x)
y = to_categorical(y)
y = np.squeeze(y, axis=-1)

model = Seq()
model.add(LSTM(128, activation='relu', input_shape=(max_length, len(char_to_int) + 1), return_sequences=True))
model.add(Dropout(0.1))  # Parameter to avoid overfitting
model.add(Dense(len(char_to_int) + 1, activation='sigmoid'))  # Softmax tend to work better to values that are close to 1, 
#  but since the parameters were converted to binary characters, sigmoid works better on this situations
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])  # Mean Square Error made a huge difference in question of performance... Made it start the training from 195 loss to barely 0.3 loss
model.load_weights('model.h5')
# If you wanna train the model even more(It has 94.5% accuracy and loss of 10^-4 but you can optimize it):
# model.fit(X, Y, batch_size=ANY, epochs=ANY)
# model.save_weights('model.h5')


# Function to determinate the temperature of the generated values:
def sample(preds, temperature):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_name(seed_txt: str, temperature: float = 1.0, times: int = 1):
    while True:
        generated = ""
        for i in range(random.randint(3, max_length - len(seed_txt))):  # Random values were inserted to always make different names with different lengths
            x_pred = np.zeros((1, max_length, len(char_to_int.keys()) + 1))
            for t, char in enumerate(seed_txt.lower()):
                x_pred[0, t, char_to_int[char]] = 1.0  # Make sure all characters from seed_txt are being highlighted
            preds = model.predict(x_pred, verbose=0)[0][0]
            next_index = sample(preds, temperature)
            if next_index == 0:
                next_char = list(char_to_int.keys())[0]  # Replaces the " " string
            else:
                next_char = list(char_to_int.keys())[list(char_to_int.values()).index(next_index)]  #Get the string of the index
                if next_char in ['', "'", '-']:  # Remove special characters
                    continue
            generated += next_char  
        generated_check = re.findall(r'[bcdfghjklmnpqrstvwxyz]+', generated, re.IGNORECASE)  # Check all consonant cases, since the bot tends to generate them way too much... 
        #  It's not their fault tho, we have like 5 vowels and 21 consonants.

        def coc(string):
            return bool(re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', string, re.IGNORECASE))  # Check if all the generated characters are only consonants... This was added to avoid generate gibberish more frequently.
        for item in generated_check:
            if len(generated_check) == 1 and len(item) <= 2 and coc(generated) is False:
                if item.endswith(end_of_names):  # Remember the end_of_names? Here's its usage
                    return f"{seed_txt}{generated.replace(' ', '')}"
