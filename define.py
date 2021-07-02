#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:15:22 EDT 2021

author: Ryan Hildebrandt
"""

# %% Doc setup
import pandas as pd

from prep import kj_dict
from scrape import jmd_meanings, jmd_readings

# %% read yoji_out
yoji_out = open("./yoji_out.txt").read().splitlines()

# %% yoji_out_df building
yoji_out_df = pd.DataFrame()
yoji_out_df["yoji"] = yoji_out

for j in range(1,5):
	yoji_out_df[f'j{j}'] = [i[j-1:j] for i in yoji_out_df["yoji"]]
	yoji_out_df[f'j{j}_Meanings'] = [kj_dict[i]['Meanings'] if i else None for i in yoji_out_df[f'j{j}']]
	yoji_out_df[f'j{j}_Readings'] = [kj_dict[i]['Readings'] if i else None for i in yoji_out_df[f'j{j}']]

# for bigrams within the 4 char compounds
for j in [1,3]:
	yoji_out_df[f'j{j}{j+1}'] = yoji_out_df[f'j{j}'] + yoji_out_df[f'j{j+1}'] 
	yoji_out_df[f'j{j}{j+1}_Meanings'] = [jmd_meanings(i) for i in yoji_out_df[f'j{j}{j+1}']]
	yoji_out_df[f'j{j}{j+1}_Readings'] = [jmd_readings(i) for i in yoji_out_df[f'j{j}{j+1}']]

print(yoji_out_df)
yoji_out_df.to_csv("./yoji_out_df.csv")

