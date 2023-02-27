import random
import numpy as np
import re
from model_creator import model
from preprocessing import max_length, char_to_int
from tensorflow.python.ops.numpy_ops.np_random import seed

seed(42)  # Set seed for fixing values

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')  # Takes the preds value and convert to float
    preds = np.log(preds) / temperature  # Then it takes the logarithm of the same preds and divide by temperature, to generate different values
    exp_preds = np.exp(preds) 
    preds = exp_preds / np.sum(exp_preds)  # Then it takes the exponential of preds and divide by the sum of the same exponentials
    probas = np.random.multinomial(1, preds, 1)  # Generates an array with possible values to be used
    return np.argmax(probas)  # And finally return the index of the max value


def generate_name(seed_txt: str, temperature: float = 1.0, times: int = 1):
    while True:
        generated = ""
        for i in range(random.randint(3, max_length - len(seed_txt))):  # Used to create a varied range of numbers
            x_pred = np.zeros((1, max_length, len(char_to_int.keys()) + 1)) 
            for t, char in enumerate(seed_txt.lower()):
                x_pred[0, t, char_to_int[char]] = 1.0  # Convert the values of the model shape to 0 
                #  and then convert the values from the position of characters of seed_txt to 1, for working with predictions correcty
            preds = model.predict(x_pred, verbose=0)[0][0]
            next_index = sample(preds, temperature)
            if next_index == 0:  # Replace the " " string to the first string of char_to_int
                next_char = list(char_to_int.keys())[0]
            else:
                next_char = list(char_to_int.keys())[list(char_to_int.values()).index(next_index)]
                if next_char in ['', "'", '-']:  # Ignore special characters
                    continue
            generated += next_char
        generated_check = re.findall(r'[bcdfghjklmnpqrstvwxyz]+', generated, re.IGNORECASE)  # Check all consonants

        def contains_only_consonants(string):
            return bool(re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', string, re.IGNORECASE))  # Check if the generated parameter only returned consonants
        for item in generated_check:
            if len(generated_check) == 1 and len(item) <= 2 and contains_only_consonants(generated) is False:
                if item.endswith(end_of_names):  # Check if the generated name ends with the most common letters to end names
                    return f"{seed_txt}{generated.replace(' ', '')}"
