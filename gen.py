#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 19:57:09 EDT 2021

author: Ryan Hildebrandt
"""

# %% Doc setup
import numpy as np
import random
import tensorflow as tf

from prep import tokenizer, yj_dict

# %% model load
model = tf.keras.models.load_model('./outputs/myModel.h5')
model.reset_states() 

# %% Generate Sequences
sample = random.choice(list(yj_dict.keys()))
sample_vector = [tokenizer[s] for s in sample]
predicted = sample_vector

#  convert into tensor of required dimensions
sample_tensor = tf.expand_dims(sample_vector, 0) 
sample_tensor = tf.convert_to_tensor(np.repeat(sample_tensor, 64, axis=0))

# predict next 1000 characters
temperature = 0.7
desired_num = 100
num_char = 4*(desired_num+1)

for i in range(num_char):
    pred = model(sample_tensor)
    # reduce unnecessary dimensions
    pred = pred[0].numpy()/temperature
    pred = tf.random.categorical(pred, num_samples=1)[-1,0].numpy()
    predicted.append(pred)
    sample_tensor = predicted[-99:]
    sample_tensor = tf.expand_dims([pred],0)
    # broadcast to first dimension to 64 
    sample_tensor = tf.convert_to_tensor(np.repeat(sample_tensor, 64, axis=0))

# convert the integers back to characters and split
pred_char = [list(tokenizer.keys())[list(tokenizer.values()).index(i)] for i in predicted]
generated = ["".join(pred_char)[i:i+4] for i in range(0,num_char,4)]
generated = [i for i in generated if not i in list(yj_dict.keys())]
print(generated)

yoji_out = "\n".join(generated)

with open('./outputs/yoji_out.txt', 'w') as f:
	f.write(yoji_out)
