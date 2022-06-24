#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 16:11:54 EDT 2021

author: Ryan Hildebrandt
"""

# %% Doc setup
#https://github.com/RajkumarGalaxy/NLP/blob/master/beginners-guide-to-text-generation-with-rnns.ipynb
import pickle
import tensorflow as tf

with open("./outputs/scraped_data.pickle", "rb") as f:
    kj_dict, kj_list, yj_dict, yoji_df, bg_list, bg_dict = pickle.load(f)

# %% prep yoji_df
tokenizer = {char:i for i,char in enumerate(kj_list)}
tokenized = [[tokenizer[i] for i in j] for j in yoji_df.yoji]
sequences = tf.data.Dataset.from_generator(lambda: tokenized, tf.int32, output_shapes=tf.TensorShape(4,))

def prepare_dataset(seq):
	input_vector = seq[:-1]
	target_vector = seq[1:]
	return input_vector, target_vector

dataset = sequences.map(prepare_dataset)

AUTOTUNE = tf.data.experimental.AUTOTUNE
data_prepped = dataset.batch(64, drop_remainder=True).repeat()
data_prepped = data_prepped.prefetch(AUTOTUNE)
