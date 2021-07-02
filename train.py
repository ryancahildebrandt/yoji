#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:14:49 EDT 2021

author: Ryan Hildebrandt
"""

# %% Doc setup
#https://github.com/RajkumarGalaxy/NLP/blob/master/beginners-guide-to-text-generation-with-rnns.ipynb
import pickle

from prep import data_prepped, sequences
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Embedding, LSTM

with open("./scraped_data.pickle", "rb") as f:
    kj_dict, kj_list, yj_dict, yoji_df = pickle.load(f)

# %% model config
spe = len(list(sequences))//64

model = keras.Sequential([
		 # Embed len(vocabulary) into 64 dimensions
		 Embedding(len(kj_list), 64, batch_input_shape=[64,None]),
		 # LSTM RNN layers
		 LSTM(352, return_sequences=True, stateful=True),
		 Dropout(.2),
		 LSTM(352, return_sequences=True, stateful=True),
		 Dropout(.2),
		 # Classification head
		 Dense(len(kj_list))
 ])
model.summary() 

model.compile(
	optimizer=keras.optimizers.Adam(learning_rate=0.0001), 
	loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
	metrics=[keras.metrics.SparseCategoricalAccuracy()])

# %% model train
h = model.fit(
	data_prepped, 
	epochs=10, 
	steps_per_epoch=spe) 

print(h.history)
print(f"min loss: {min(h.history['loss'])}")
print(f"accuracy range: {min(h.history['sparse_categorical_accuracy'])} - {max(h.history['sparse_categorical_accuracy'])}")

model.save('./myModel.h5')

