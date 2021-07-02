#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 20:27:48 EDT 2021

author: Ryan Hildebrandt
"""

# %% Doc setup
import pickle

from kerastuner import RandomSearch
from prep import data_prepped, sequences
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Embedding, LSTM

STEPS_PER_EPOCH = len(list(sequences))//64

with open("./scraped_data.pickle", "rb") as f:
    kj_dict, kj_list, yj_dict, yoji_df = pickle.load(f)

def build_model(hp):
    model = keras.Sequential([
		 # Embed len(vocabulary) into 64 dimensions
		 Embedding(len(kj_list), 64, batch_input_shape=[64,None]),
		 # LSTM RNN layers
		 LSTM(units=hp.Int("units", min_value=32, max_value=512, step=32), return_sequences=True, stateful=True),
		 Dropout(.2),
		 LSTM(units=hp.Int("units", min_value=32, max_value=512, step=32), return_sequences=True, stateful=True),
		 Dropout(.2),
		 # Classification head
		 Dense(len(kj_list), activation='softmax')
		 ])

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice("learning_rate", values=[1e-1, 1e-2, 1e-3, 1e-4])
        ),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[
        keras.metrics.SparseCategoricalAccuracy()
        ])
    return model

tuner = RandomSearch(
    build_model,
    objective='sparse_categorical_accuracy',
    max_trials=5,
    executions_per_trial=3,
    overwrite=True,
    directory="./hp_tuning",
    project_name="yoji_model")

tuner.search_space_summary()
tuner.search(
	data_prepped, 
	epochs=10, 
	steps_per_epoch=STEPS_PER_EPOCH)

best_models = tuner.get_best_models(num_models=3)
tuner.results_summary()
best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

print(f"""
The hyperparameter search is complete. The optimal number of units in the first densely-connected
layer is {best_hps.get('units')} and the optimal learning rate for the optimizer
is {best_hps.get('learning_rate')}.
""")
