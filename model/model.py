import os
from preprocessing import max_length, char_to_int
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Removes unnecessary compiler warning. 

model = Sequential()  # Create a simple model
model.add(LSTM(128, activation='relu', input_shape=(max_length, len(char_to_int) + 1), return_sequences=True))
model.add(Dropout(0.1))  # Randomly set 10% of the values to 0 to avoid overfitting
model.add(Dense(len(char_to_int) + 1, activation='sigmoid'))  # Sigmoid function works better with numbers between 0 and 1 than softmax
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])  # MSE or Mean Squared Error basically measures the average squared difference 
#  between the estimated values and true value, which works properly on string parameters that were converted into 
#  integers rather than categorical crossentropy, which would be the normal usage
model.load_weights('model.h5')
