# Wisdom in 4 Characters Or Less

---
![Training a neural network to generate 四字熟語 (as best it can!)](./outputs/header.jpg)

---
[![Open in gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/ryancahildebrandt/yoji)
[![This project contains 0% LLM-generated content](https://brainmade.org/88x31-dark.png)](https://brainmade.org/)

## *Purpose*

A project to generate 四字熟語 (yoji-jukugo, 4 character Japanese idioms), using a sequential tensorflow model.

---
## *Dataset*
The dataset used for the current project was scraped/pulled from the following: 
- [Yojijukugo](http://www.edrdg.org/projects/yojijukugo.html) for idioms and meanings/readings
- [Jamdict](https://github.com/neocl/jamdict) for kanji readings, meanings, and other information
- [Kanji Database](https://www.kanjidatabase.com/) for kanji classification, grade level, and misc characteristics 

---

## *Outputs*

+ The main [report](https://datapane.com/u/ryancahildebrandt/reports/wisdom-in-4-characters/), compiled with datapane and also in [html](./outputs/yoji_rprt.html) format
+ The full [yoji_df](./outputs/yoji_df.csv) dataframe describing the idioms, their constituent kanji, and all additional characteristics from the data linked above
+ List of generated [idioms](./outputs/yoji_out.txt), sans definitions and readings
+ The same list, expanded out to a [dataframe](./outputs/yoji_out_df.csv) including readings and meanings of constituent characters and bigrams 

---

## *Update!*

+ After sharing the initial project with some coworkers, it was suggested (by @DC & @JZ) that I retrain the model on bigrams within each idiom, as this more closely aligns with how yoji-jukugo are semantically divided and understood. I've updated the report linked above with some additional thoughts on the new model and its results!
