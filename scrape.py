#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 20:51:09 EDT 2021

author: Ryan Hildebrandt
"""

# Doc setup
import pandas as pd
import pickle
import re
import requests

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from itertools import compress
from jamdict import Jamdict

# Functions
def jmd_char_lookup(kanji):
	out = jmd.lookup(kanji).chars if len(kanji)!=0 else ":0:"
	return out

def jmd_char_main(kanji):
	ind = [kanji in i for i in kj_chars]
	res = compress(kj_chars, ind)
	out = [i for i in res]
	return out[0] if len(out)==1 else [None,"0",None]

def jmd_readings(kanji):
	res = jmd.lookup(kanji)
	r = re.findall(r"[ぁ-ん]*",str(res.entries))
	r = list(filter(None, r))
	return r

def jmd_meanings(kanji):
	res = jmd.lookup(kanji)
	m = re.split("[ぁ-ん一-龯々\(\)\[\] ]*?:", str(res.entries))
	m = [re.split(" \d\.", i) for i in m]
	m = list(filter(None, [''.join(i) for i in m]))
	m = [re.sub("[,\]\[]]$", "", i) for i in m]
	m = list(filter(None, m))
	return m

def kdb_att_lookup(kanji, att):
	indx = kdb_kanji.index[kdb_kanji.Kanji==kanji]
	res = kdb_kanji[att][indx].tolist()
	out = None if len(res)==0 else res
	return out

# KDB & JMD lookups
jmd = Jamdict()
kdb_kanji = pd.read_csv("./data/Kanji_20201227_151030.csv", sep=";")[['Kanji','Grade','Kanji Classification','JLPT-test','Kanji Frequency with Proper Nouns','Kanji Frequency without Proper Nouns','Symmetry']]

# Yoji scrape
yoji_page = requests.get("http://www.edrdg.org/projects/yojijukugo.html")
yoji_soup = BeautifulSoup(yoji_page.content, "html.parser", parse_only=SoupStrainer("td"))
yoji_list = [i.get_text() for i in yoji_soup if len(i.get_text())>4]
yoji_filter = [(len(i)>2) for i in [re.findall(r"[一-龯々]{3,4}|$",i)[0] for i in yoji_list]]
yoji_list = list(compress(yoji_list,yoji_filter))

# yoji dict building
yj_list = [re.findall(r"[一-龯々]{3,4}|$",i)[0].ljust(4) for i in yoji_list]

yj_pos = [re.findall(r"\([a-z,-]*\)|$",i)[0] for i in yoji_list]
yj_pos = [re.sub(r"\(|\)","",i).split() for i in yj_pos]
yj_kana = [re.findall(r"\[[ぁ-ん]*\]|$",i)[0] for i in yoji_list]
yj_kana = [re.sub("\[|\]", "", i) for i in yj_kana]

yj_dict = {yj_list[i]:{"pos":yj_pos[i], "reading":yj_kana[i]} for i in range(len(yj_list))}

# bigrams
bg_list = [[i[:2],i[2:]] for i in yj_list]
bg_list = [i for j in bg_list for i in j]
bg_list = sorted(set(bg_list))

bg_dict = {bg_list[i]:{"Meanings":jmd_meanings(bg_list[i]) if bg_list[i] != " " else [" "],"Readings":jmd_readings(bg_list[i]) if bg_list[i] != " " else [" "]} for i in range(len(bg_list))}

# kanji dict building
kj_list = sorted(set(' '.join(yj_list)))
kj_chars = [re.findall(r"([一-龯々]:\d+:[a-zA-Z, -]*)|$", str(jmd_char_lookup(i))) for i in kj_list] 
kj_chars = [i[0].split(":") for i in kj_chars]+[["々","3","kanji repetition mark"]]

kj_dict = {
i:{
"Index":ind, 
"Strokes":int(jmd_char_main(i)[1]) if i != " " else [" "],
"Meanings":jmd_meanings(i) if i != " " else [" "],
"Readings":jmd_readings(i) if i != " " else [" "],
"krad":["々"] if i == "々" else ([" "] if i == " " else jmd.krad[i]),
"Kanji":kdb_att_lookup(i,"Kanji") if i != " " else [" "],
"Grade":kdb_att_lookup(i,"Grade") if i != " " else [" "],
"Kanji Classification":kdb_att_lookup(i,"Kanji Classification") if i != " " else [" "],
"JLPT-test":kdb_att_lookup(i,"JLPT-test") if i != " " else [" "],
"Kanji Frequency with Proper Nouns":kdb_att_lookup(i,"Kanji Frequency with Proper Nouns") if i != " " else [" "],
"Kanji Frequency without Proper Nouns":kdb_att_lookup(i,"Kanji Frequency without Proper Nouns") if i != " " else [" "],
"Symmetry":kdb_att_lookup(i,"Symmetry") if i != " " else [" "]
} for ind,i in enumerate(kj_list)}

kj_df = pd.DataFrame.from_dict(kj_dict, orient = "index")

# yoji_df building
yoji_df = pd.DataFrame()
yoji_df["yoji"] = yj_dict.keys()
yoji_df["yj_pos"] = [i["pos"] for i in yj_dict.values()]
yoji_df["yj_reading"] = [i["reading"] for i in yj_dict.values()]

for j in range(1,5):
	yoji_df[f'j{j}'] = [i[j-1:j] for i in yoji_df["yoji"]]
	for k in list(kj_dict["心"].keys()):
		yoji_df[f'j{j}_{k}'] = [kj_dict[i][k] if i else None for i in yoji_df[f'j{j}']]

yoji_df["bg1"] = [i[:2] for i in yoji_df["yoji"]]
yoji_df["bg1_Meanings"] = [bg_dict[i]["Meanings"] for i in yoji_df["bg1"]]
yoji_df["bg1_Readings"] = [bg_dict[i]["Readings"] for i in yoji_df["bg1"]]
yoji_df["bg2"] = [i[:2] for i in yoji_df["yoji"]]
yoji_df["bg2_Meanings"] = [bg_dict[i]["Meanings"] for i in yoji_df["bg2"]]
yoji_df["bg2_Readings"] = [bg_dict[i]["Readings"] for i in yoji_df["bg2"]]

yoji_df.to_csv("./outputs/yoji_df.csv")
kj_df.to_csv("./outputs/kj_df.csv")

yoji_df_missing = yoji_df[yoji_df.isnull().any(axis=1)]
yoji_df_missing.to_csv("./outputs/yoji_df_missing.csv")

with open("./outputs/scraped_data.pickle", 'wb') as f:
	pickle.dump([kj_dict, kj_list, yj_dict, yoji_df, bg_list, bg_dict], f)

